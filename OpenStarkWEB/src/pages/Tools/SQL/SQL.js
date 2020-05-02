import React, { Component } from 'react';
import router from 'umi/router';
import { connect } from 'dva';
import { Menu } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from '../style.less';

const { Item } = Menu;

@connect(({ tools, global }) => ({
  sqlList: tools.sqlList,
  collapsed: global.collapsed,
}))
class SQL extends Component {
  constructor(props) {
    super(props);
    const { match, location } = props;
    const menuMap = {
      0: '自定义SQL',
    };
    const key = location.pathname.replace(`${match.path}/`, '');
    this.state = {
      mode: 'inline',
      menuMap,
      selectKey: menuMap[key] ? key : '0',
    };
  }

  static getDerivedStateFromProps(props, state) {
    const { sqlList, match, location } = props;
    const menus = {};
    let key = '0';
    sqlList.forEach(item => {
      menus[item.id] = item.title;
      key = item.id;
    });
    let selectKey = location.pathname.replace(`${match.path}/`, '');
    selectKey = state.menuMap[selectKey] || menus[selectKey] ? selectKey : key;
    if (selectKey !== state.selectKey || menus !== state.menuMap) {
      return { selectKey, menuMap: menus };
    }
    return null;
  }

  componentDidMount() {
    const { dispatch, collapsed } = this.props;
    dispatch({
      type: 'tools/getSQL',
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
    return menuMap[selectKey];
  };

  selectKey = ({ key }) => {
    router.push(`/tools/scripts/sql/${key}`);
    this.setState({
      selectKey: key,
    });
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/getSQL',
      payload: { id: key },
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
            <div className={styles.title}>{this.getRightTitle()}</div>
            {children}
          </div>
        </div>
      </PageHeaderWrapper>
    );
  }
}

export default SQL;
