import React, { PureComponent } from 'react';
import router from 'umi/router';
import { connect } from 'dva';
import { Menu } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from '../../Tools/style.less';

const { Item } = Menu;

@connect(({ knowledge, global }) => ({
  knowledge,
  collapsed: global.collapsed,
}))
class BlogList extends PureComponent {
  constructor(props) {
    super(props);
    const { match, location } = props;
    const menuMap = {
      '0': '知识空白',
    };
    const key = location.pathname.replace(`${match.url}/`, '');
    this.state = {
      mode: 'inline',
      menuMap,
      selectKey: menuMap[key] ? key : '0',
    };
  }

  static getDerivedStateFromProps(props, state) {
    const {
      knowledge: { blogList },
      match,
      location,
    } = props;
    const menus = {};
    let key = '0';
    blogList.forEach(item => {
      menus[item.id] = item.title;
      key = item.id;
    });
    let selectKey = location.pathname.replace(`${match.url}/`, '');
    selectKey = state.menuMap[selectKey] || menus[selectKey] ? selectKey : key;
    if (selectKey !== state.selectKey || menus !== state.menuMap) {
      return {
        selectKey: selectKey !== '0' ? selectKey : key,
        menuMap: Object.keys(menus).length > 0 ? menus : { '0': '知识空白' },
      };
    }
    return null;
  }

  componentDidMount() {
    const {
      dispatch,
      match: { params },
      collapsed,
    } = this.props;
    dispatch({
      type: 'knowledge/getBooks',
      op: 'book',
      action: 'list',
      payload: { cateId: params.cid },
    });
    dispatch({
      type: 'knowledge/getBooks',
      op: 'cate',
      action: 'list',
    });
    window.addEventListener('resize', this.resize);
    if (collapsed) {
      dispatch({
        type: 'global/changeLayoutCollapsed',
        payload: collapsed,
      });
    }
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.resize);
  }

  getmenu = () => {
    const { menuMap } = this.state;
    return Object.keys(menuMap).map(item => <Item key={item}>{menuMap[item]}</Item>);
  };

  getRightTitle = () => {
    const { selectKey, menuMap } = this.state;
    const {
      knowledge: { blogContent },
    } = this.props;
    return blogContent.title || menuMap[selectKey];
  };

  selectKey = ({ key }) => {
    const {
      dispatch,
      match: { params },
    } = this.props;
    router.push(`/knowledge/books/blog/${params.cid}/${key}`);
    this.setState({
      selectKey: key,
    });
    dispatch({
      type: 'knowledge/getBooks',
      op: 'book',
      action: 'single',
      payload: { bid: key },
    });
  };

  resize = () => {
    if (!this.main) {
      return;
    }
    requestAnimationFrame(() => {
      let mode = 'inline';
      const { offsetWidth } = this.main;
      if (offsetWidth < 641 && offsetWidth > 400) {
        mode = 'horizontal';
      }
      if (window.innerWidth < 768 && offsetWidth > 400) {
        mode = 'horizontal';
      }
      this.setState({
        mode,
      });
    });
  };

  render() {
    const { children } = this.props;
    const { mode, selectKey } = this.state;
    return (
      <PageHeaderWrapper>
        <div
          className={styles.main}
          ref={ref => {
            this.main = ref;
          }}
        >
          <div className={styles.leftmenu}>
            <Menu mode={mode} selectedKeys={[selectKey]} onClick={this.selectKey}>
              {this.getmenu()}
            </Menu>
          </div>
          <div className={styles.right}>
            <div className={styles.title}>
              <h2>{this.getRightTitle()}</h2>
            </div>
            {children}
          </div>
        </div>
      </PageHeaderWrapper>
    );
  }
}

export default BlogList;
