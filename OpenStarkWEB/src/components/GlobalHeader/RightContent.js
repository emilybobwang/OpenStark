import React, { PureComponent } from 'react';
import { FormattedMessage, formatMessage } from 'umi/locale';
import { Spin, Tag, Menu, Icon, Avatar, Tooltip, Modal } from 'antd';
import moment from 'moment';
import groupBy from 'lodash/groupBy';
import Sockette from 'sockette';
import NoticeIcon from '../NoticeIcon';
import HeaderDropdown from '../HeaderDropdown';
// import SelectLang from '../SelectLang';
import styles from './index.less';

export default class GlobalHeaderRight extends PureComponent {
  state = {
    visible: false,
    ws: null,
    content: [],
  };

  getNoticeData() {
    const { notices = [] } = this.props;
    if (notices.length === 0) {
      return {};
    }
    const newNotices = notices.map(notice => {
      const newNotice = { ...notice };
      if (newNotice.datetime) {
        newNotice.datetime = moment(notice.datetime).fromNow();
      }
      if (newNotice.id) {
        newNotice.key = newNotice.id;
      }
      if (newNotice.extra && newNotice.status) {
        const color = {
          todo: '',
          processing: 'blue',
          urgent: 'red',
          doing: 'gold',
        }[newNotice.status];
        newNotice.extra = (
          <Tag color={color} style={{ marginRight: 0 }}>
            {newNotice.extra}
          </Tag>
        );
      }
      return newNotice;
    });
    return groupBy(newNotices, 'type');
  }

  getUnreadData = noticeData => {
    const unreadMsg = {};
    Object.entries(noticeData).forEach(([key, value]) => {
      if (!unreadMsg[key]) {
        unreadMsg[key] = 0;
      }
      if (Array.isArray(value)) {
        unreadMsg[key] = value.filter(item => !item.read).length;
      }
    });
    return unreadMsg;
  };

  openLogs = () => {
    const ws = new Sockette(`ws://${window.location.host}/api/py/ws/weblogs`, {
      timeout: 5000,
      maxAttempts: 10,
      onopen: e => {
        e.target.send('get_logs');
      },
      onmessage: e => {
        const { content } = this.state;
        content.push({ id: content.length, data: e.data });
        this.setState({ content: content.map(item => item) });
        const div = window.document.getElementsByClassName('ant-modal-body');
        if (div.length > 0) {
          div[0].scrollTop = div[0].scrollHeight;
        }
      },
      onclose: e => {
        e.target.close();
        const { content } = this.state;
        content.push({ id: content.length, data: 'WebSocket closed' });
        this.setState({ ws: null, content: content.map(item => item) });
      },
      onerror: e => {
        e.target.close();
        const { content } = this.state;
        content.push({ id: content.length, data: 'Connection WebSocket service error' });
        this.setState({ content: content.map(item => item) });
      },
    });
    this.setState({ visible: true, ws });
  };

  closeLogs = () => {
    const { ws } = this.state;
    if (ws) {
      ws.close(1000);
    }
    this.setState({ visible: false, ws: null, content: [{ id: 0, data: '' }] });
  };

  changeReadState = clickedItem => {
    const { id } = clickedItem;
    const { dispatch } = this.props;
    dispatch({
      type: 'global/changeNoticeReadState',
      payload: id,
    });
  };

  fetchMoreNotices = tabProps => {
    const { list, name } = tabProps;
    const { dispatch, notices = [] } = this.props;
    const lastItemId = notices[notices.length - 1].id;
    dispatch({
      type: 'global/fetchMoreNotices',
      payload: {
        lastItemId,
        type: name,
        offset: list.length,
      },
    });
  };

  render() {
    const {
      currentUser,
      fetchingMoreNotices,
      fetchingNotices,
      loadedAllNotices,
      onNoticeVisibleChange,
      onMenuClick,
      onNoticeClear,
      skeletonCount,
      theme,
    } = this.props;
    const menu = (
      <Menu className={styles.menu} selectedKeys={[]} onClick={onMenuClick}>
        {/* <Menu.Item key="userCenter">
          <Icon type="user" />
          <FormattedMessage id="menu.account.center" defaultMessage="account center" />
        </Menu.Item> */}
        <Menu.Item key="userinfo">
          <Icon type="setting" />
          <FormattedMessage id="menu.account.settings" defaultMessage="account settings" />
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item key="logout">
          <Icon type="logout" />
          <FormattedMessage id="menu.account.logout" defaultMessage="logout" />
        </Menu.Item>
      </Menu>
    );
    const loadMoreProps = {
      skeletonCount,
      loadedAll: loadedAllNotices,
      loading: fetchingMoreNotices,
    };
    const noticeData = this.getNoticeData();
    const unreadMsg = this.getUnreadData(noticeData);
    let className = styles.right;
    if (theme === 'dark') {
      className = `${styles.right}  ${styles.dark}`;
    }
    const { visible, content } = this.state;
    return (
      <div className={className}>
        <Tooltip title="日志">
          <a
            onClick={this.openLogs}
            rel="noopener noreferrer"
            className={styles.action}
            title="日志"
          >
            <Icon type="exception" />
          </a>
          <Modal
            title="系统日志"
            width="90%"
            footer={null}
            visible={visible}
            onCancel={this.closeLogs}
            style={{ top: 20 }}
            bodyStyle={{
              backgroundColor: '#006',
              maxHeight: window.document.body.clientHeight - 100,
              overflowY: 'auto',
            }}
          >
            <div style={{ color: '#fff' }}>
              {content.map(item => (
                <p key={item.id}>{item.data}</p>
              ))}
            </div>
          </Modal>
        </Tooltip>
        <Tooltip title="帮助">
          <a
            target="_blank"
            href="/home/help"
            rel="noopener noreferrer"
            className={styles.action}
            title="帮助"
          >
            <Icon type="question-circle-o" />
          </a>
        </Tooltip>
        <NoticeIcon
          className={styles.action}
          count={currentUser.unreadCount}
          onItemClick={(item, tabProps) => {
            this.changeReadState(item, tabProps);
          }}
          locale={{
            emptyText: formatMessage({ id: 'component.noticeIcon.empty' }),
            clear: formatMessage({ id: 'component.noticeIcon.clear' }),
            loadedAll: formatMessage({ id: 'component.noticeIcon.loaded' }),
            loadMore: formatMessage({ id: 'component.noticeIcon.loading-more' }),
          }}
          onClear={onNoticeClear}
          onLoadMore={this.fetchMoreNotices}
          onPopupVisibleChange={onNoticeVisibleChange}
          loading={fetchingNotices}
          clearClose
        >
          <NoticeIcon.Tab
            count={unreadMsg.notification}
            list={noticeData.notification}
            title={formatMessage({ id: 'component.globalHeader.notification' })}
            name="notification"
            emptyText={formatMessage({ id: 'component.globalHeader.notification.empty' })}
            emptyImage="https://gw.alipayobjects.com/zos/rmsportal/wAhyIChODzsoKIOBHcBk.svg"
            {...loadMoreProps}
          />
          <NoticeIcon.Tab
            count={unreadMsg.message}
            list={noticeData.message}
            title={formatMessage({ id: 'component.globalHeader.message' })}
            name="message"
            emptyText={formatMessage({ id: 'component.globalHeader.message.empty' })}
            emptyImage="https://gw.alipayobjects.com/zos/rmsportal/sAuJeJzSKbUmHfBQRzmZ.svg"
            {...loadMoreProps}
          />
          <NoticeIcon.Tab
            count={unreadMsg.event}
            list={noticeData.event}
            title={formatMessage({ id: 'component.globalHeader.event' })}
            name="event"
            emptyText={formatMessage({ id: 'component.globalHeader.event.empty' })}
            emptyImage="https://gw.alipayobjects.com/zos/rmsportal/HsIsxMZiWKrNUavQUXqx.svg"
            {...loadMoreProps}
          />
        </NoticeIcon>
        {currentUser.name ? (
          <HeaderDropdown overlay={menu}>
            <span className={`${styles.action} ${styles.account}`}>
              <Avatar
                size="small"
                className={styles.avatar}
                src={currentUser.avatar}
                alt="avatar"
              />
              <span className={styles.name}>{currentUser.name}</span>
            </span>
          </HeaderDropdown>
        ) : (
          <Spin size="small" style={{ marginLeft: 8, marginRight: 8 }} />
        )}
        {/* <SelectLang className={styles.action} /> */}
      </div>
    );
  }
}
