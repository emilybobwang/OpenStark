import React, { Fragment } from 'react';
// import { formatMessage } from 'umi/locale';
import Link from 'umi/link';
import { Icon } from 'antd';
import { connect } from 'dva';
import DocumentTitle from 'react-document-title';
import GlobalFooter from '@/components/GlobalFooter';
// import SelectLang from '@/components/SelectLang';
import styles from './UserLayout.less';
import logo from '../assets/logo.svg';

const IconFont = Icon.createFromIconfontCN({
  scriptUrl: '//at.alicdn.com/t/font_1054356_ka12c4y9rgk.js',
});
const links = [
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
];

@connect(({ global }) => ({ commonInfo: global.commonInfo }))
class UserLayout extends React.PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'global/fetchCommonInfo',
    });
  }
  // @TODO title
  // getPageTitle() {
  //   const { routerData, location } = this.props;
  //   const { pathname } = location;
  //   let title = 'Ant Design Pro';
  //   if (routerData[pathname] && routerData[pathname].name) {
  //     title = `${routerData[pathname].name} - Ant Design Pro`;
  //   }
  //   return title;
  // }

  render() {
    const {
      children,
      commonInfo: { sysName, sysDesc, company },
    } = this.props;
    const title = sysName || '斯塔克综合测试管理平台';
    const desc = sysDesc || '让测试更高效 使测试更简单';
    let copyright = company || '鸥鹏斯塔克';
    copyright = (
      <Fragment>
        Copyright&nbsp;&nbsp;
        <Icon type="copyright" />
        2018-{new Date().getFullYear()}&nbsp;&nbsp;
        {copyright}
      </Fragment>
    );
    return (
      <DocumentTitle title={title}>
        <div className={styles.container}>
          <div className={styles.content}>
            <div className={styles.top}>
              <div className={styles.header}>
                <Link to="/">
                  <img alt="logo" className={styles.logo} src={logo} />
                  <span className={styles.title}>{title}</span>
                </Link>
              </div>
              <div className={styles.desc}>{desc}</div>
            </div>
            {children}
          </div>
          <GlobalFooter links={links} copyright={copyright} />
        </div>
      </DocumentTitle>
    );
  }
}

export default UserLayout;
