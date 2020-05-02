import React, { Component } from 'react';
import router from 'umi/router';
import { connect } from 'dva';
import { Menu } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from '../style.less';

const { Item } = Menu;

@connect(({ tools }) => ({
  toolsMenu: tools.toolsMenu,
}))
class Others extends Component {
  constructor(props) {
    super(props);
    const { match, location } = props;
    const menuMap = {
      '0': '还没有添加第三方工具',
    };
    const key = location.pathname.replace(`${match.path}/`, '');
    this.state = {
      mode: 'inline',
      menuMap,
      selectKey: menuMap[key] ? key : '0',
    };
  }

  static getDerivedStateFromProps(props, state) {
    const { toolsMenu, match, location } = props;
    const menus = {};
    let key = '0';
    toolsMenu.forEach(item => {
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
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/fetchToolsMenu',
    });
    window.addEventListener('resize', this.resize);
    dispatch({
      type: 'global/changeLayoutCollapsed',
      payload: true,
    });
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
    const { toolsMenu } = this.props;
    let href = '#';
    let desc = '';
    toolsMenu.forEach(item => {
      if (item.id && item.id.toString() === selectKey && selectKey.toString()) {
        href = item.url;
        desc = item.description;
      }
    });
    return (
      <div>
        <a href={href} target="_blank" rel="noopener noreferrer">
          {menuMap[selectKey]}
        </a>
        <p style={{ fontSize: 12 }}>{desc}</p>
      </div>
    );
  };

  selectKey = ({ key }) => {
    router.push(`/tools/others/${key}`);
    this.setState({
      selectKey: key,
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

export default Others;
