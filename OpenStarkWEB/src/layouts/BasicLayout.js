import React, { Fragment, Suspense } from 'react';
import { Layout, Icon } from 'antd';
import DocumentTitle from 'react-document-title';
import isEqual from 'lodash/isEqual';
import memoizeOne from 'memoize-one';
import { connect } from 'dva';
import { ContainerQuery } from 'react-container-query';
import classNames from 'classnames';
import pathToRegexp from 'path-to-regexp';
import Media from 'react-media';
import { formatMessage } from 'umi/locale';
import Authorized from '@/utils/Authorized';
import logo from '../assets/logo.svg';
import GlobalFooter from '@/components/GlobalFooter';
import Header from './Header';
import Context from './MenuContext';
import Exception403 from '../pages/Exception/403';
import PageLoading from '@/components/PageLoading';
import SiderMenu from '@/components/SiderMenu';
import { menu, title } from '../defaultSettings';

import styles from './BasicLayout.less';

// lazy load SettingDrawer
const SettingDrawer = React.lazy(() => import('@/components/SettingDrawer'));

const { Content } = Layout;
const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1054356_ka12c4y9rgk.js',
});
const query = {
  'screen-xs': {
    maxWidth: 575,
  },
  'screen-sm': {
    minWidth: 576,
    maxWidth: 767,
  },
  'screen-md': {
    minWidth: 768,
    maxWidth: 991,
  },
  'screen-lg': {
    minWidth: 992,
    maxWidth: 1199,
  },
  'screen-xl': {
    minWidth: 1200,
    maxWidth: 1599,
  },
  'screen-xxl': {
    minWidth: 1600,
  },
};

class BasicLayout extends React.Component {
  constructor(props) {
    super(props);
    this.getPageTitle = memoizeOne(this.getPageTitle);
    this.matchParamsPath = memoizeOne(this.matchParamsPath, isEqual);
  }

  componentDidMount() {
    const {
      dispatch,
      route: { routes, authority },
    } = this.props;
    dispatch({
      type: 'global/fetchCommonInfo',
    });
    dispatch({
      type: 'user/fetchCurrent',
    });
    dispatch({
      type: 'setting/getSetting',
    });
    dispatch({
      type: 'menu/getMenuData',
      payload: { routes, authority },
    });
  }

  getContext() {
    const { location, breadcrumbNameMap } = this.props;
    return {
      location,
      breadcrumbNameMap,
    };
  }

  matchParamsPath = (pathname, breadcrumbNameMap) => {
    const pathKey = Object.keys(breadcrumbNameMap).find(key => pathToRegexp(key).test(pathname));
    return breadcrumbNameMap[pathKey];
  };

  getRouteAuthority = (pathname, routeData) => {
    const routes = routeData.slice(); // clone

    const getAuthority = (routeDatas, path) => {
      let authorities;
      routeDatas.forEach(route => {
        // check partial route
        if (pathToRegexp(`${route.path}(.*)`).test(path)) {
          if (route.authority) {
            authorities = route.authority;
          }
          // is exact route?
          if (!pathToRegexp(route.path).test(path) && route.routes) {
            authorities = getAuthority(route.routes, path);
          }
        }
      });
      return authorities;
    };

    return getAuthority(routes, pathname);
  };

  getPageTitle = (pathname, breadcrumbNameMap) => {
    const {
      commonInfo: { sysName },
    } = this.props;
    const currRouterData = this.matchParamsPath(pathname, breadcrumbNameMap);

    if (!currRouterData) {
      return sysName || title;
    }
    const pageName = menu.disableLocal
      ? currRouterData.name
      : formatMessage({
          id: currRouterData.locale || currRouterData.name,
          defaultMessage: currRouterData.name,
        });

    return `${pageName} - ${sysName || title}`;
  };

  getLayoutStyle = () => {
    const { fixSiderbar, isMobile, collapsed, layout } = this.props;
    if (fixSiderbar && layout !== 'topmenu' && !isMobile) {
      return {
        paddingLeft: collapsed ? '80px' : '256px',
      };
    }
    return null;
  };

  handleMenuCollapse = collapsed => {
    const { dispatch } = this.props;
    dispatch({
      type: 'global/changeLayoutCollapsed',
      payload: collapsed,
    });
  };

  renderSettingDrawer = () => {
    // Do not render SettingDrawer in production
    // unless it is deployed in preview.pro.ant.design as demo
    if (process.env.NODE_ENV === 'production' && APP_TYPE !== 'site') {
      return null;
    }
    return <SettingDrawer />;
  };

  render() {
    const {
      navTheme,
      layout: PropsLayout,
      children,
      location: { pathname },
      commonInfo: { company },
      isMobile,
      menuData,
      breadcrumbNameMap,
      route: { routes },
      fixedHeader,
    } = this.props;

    const isTop = PropsLayout === 'topmenu';
    const routerConfig = this.getRouteAuthority(pathname, routes);
    const contentStyle = !fixedHeader ? { paddingTop: 0 } : {};
    const layout = (
      <Layout>
        {isTop && !isMobile ? null : (
          <SiderMenu
            logo={logo}
            theme={navTheme}
            onCollapse={this.handleMenuCollapse}
            menuData={menuData}
            isMobile={isMobile}
            {...this.props}
          />
        )}
        <Layout
          style={{
            ...this.getLayoutStyle(),
            minHeight: '100vh',
          }}
        >
          <Header
            menuData={menuData}
            handleMenuCollapse={this.handleMenuCollapse}
            logo={logo}
            isMobile={isMobile}
            {...this.props}
          />
          <Content className={styles.content} style={contentStyle}>
            <Authorized authority={routerConfig} noMatch={<Exception403 />}>
              {children}
            </Authorized>
          </Content>
          <GlobalFooter
            links={[
              {
                key: 'blog',
                title: <IconFont type="icon-wordpress" />,
                href: 'https://www.bstester.com/',
                blankTarget: true,
              },
              {
                key: 'github',
                title: <Icon type="github" />,
                href: 'https://github.com/BSTester',
                blankTarget: true,
              },
            ]}
            copyright={
              <Fragment>
                Copyright&nbsp;&nbsp;
                <Icon type="copyright" />
                2018-{new Date().getFullYear()}&nbsp;&nbsp;
                {company}
              </Fragment>
            }
          />
        </Layout>
      </Layout>
    );
    return (
      <React.Fragment>
        <DocumentTitle title={this.getPageTitle(pathname, breadcrumbNameMap)}>
          <ContainerQuery query={query}>
            {params => (
              <Context.Provider value={this.getContext()}>
                <div className={classNames(params)}>{layout}</div>
              </Context.Provider>
            )}
          </ContainerQuery>
        </DocumentTitle>
        <Suspense fallback={<PageLoading />}>{this.renderSettingDrawer()}</Suspense>
      </React.Fragment>
    );
  }
}

export default connect(({ global, setting, menu: menuModel }) => ({
  collapsed: global.collapsed,
  commonInfo: global.commonInfo,
  layout: setting.layout,
  menuData: menuModel.menuData,
  breadcrumbNameMap: menuModel.breadcrumbNameMap,
  ...setting,
}))(props => (
  <Media query="(max-width: 599px)">
    {isMobile => <BasicLayout {...props} isMobile={isMobile} />}
  </Media>
));
