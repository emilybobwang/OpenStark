import React, { PureComponent } from 'react';
import moment from 'moment';
import { connect } from 'dva';
import { Row, Col, Card, List, Avatar, Modal, Form, Input, Tooltip, Divider } from 'antd';
import EditableLinkGroup from '@/components/EditableLinkGroup';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from './Workplace.less';

const FormItem = Form.Item;

@connect(({ project, activities, chart, user, loading }) => ({
  user,
  project,
  activities,
  chart,
  projectLoading: loading.effects['project/fetchNotice'],
  activitiesLoading: loading.effects['activities/fetchList'],
  addLinkLoading: loading.effects['user/addLink'],
}))
@Form.create()
class Workplace extends PureComponent {
  state = {
    visible: false,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'activities/fetchList',
    });
    dispatch({
      type: 'user/getLink',
    });
  }

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  addLink = e => {
    const { dispatch, form } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'user/addLink',
          payload: {
            type: 'navLink',
            data: values,
          },
          callback: ()=>{
            this.cancel();
            form.resetFields();
            dispatch({
              type: 'user/getLink',
            });
          },
        });
      }
    });
  };

  cancel = () => {
    this.setState({
      visible: false,
    });
  };

  renderActivities() {
    const {
      activities: { list },
    } = this.props;
    return list.map(item => {
      const events = item.template.split(/@\{([^{}]*)\}/gi).map(key => {
        if (item[key]) {
          return (
            <a href={item[key].link} key={item[key].name}>
              {item[key].name}
            </a>
          );
        }
        return key;
      });
      return (
        <List.Item key={item.id}>
          <List.Item.Meta
            avatar={<Avatar src={item.user.avatar} />}
            title={
              <span>
                <a className={styles.username}>{item.user.name}</a>
                &nbsp;
                <span className={styles.event}>{events}</span>
              </span>
            }
            description={
              <span className={styles.datetime} title={item.updatedAt}>
                {moment(item.updatedAt).fromNow()}
              </span>
            }
          />
        </List.Item>
      );
    });
  }

  renderBlogs() {
    const {
      activities: { blogs, users },
    } = this.props;
    return blogs.map(item => {
      const events = item.template.split(/@\{([^{}]*)\}/gi).map(key => {
        if (item[key]) {
          return (
            <a href={item[key].link} key={item[key].name}>
              {item[key].name}
            </a>
          );
        }
        return key;
      });
      let avatar = users.filter(key => key.uid === item.uid);
      avatar = avatar.length > 0 && avatar[0];
      return (
        <List.Item key={item.id}>
          <List.Item.Meta
            avatar={<Avatar src={avatar && avatar.avatar} />}
            title={
              <span>
                <a className={styles.username}>{avatar && avatar.name}</a>
                &nbsp;
                <span className={styles.event}>{events}</span>
              </span>
            }
            description={
              <span className={styles.datetime} title={item.updatedAt}>
                {moment(item.updatedAt).fromNow()}
              </span>
            }
          />
        </List.Item>
      );
    });
  }

  render() {
    const {
      activitiesLoading,
      addLinkLoading,
      user: { currentUser, navLinks },
      form,
      activities: { users },
    } = this.props;
    const { getFieldDecorator } = form;
    const pageHeaderContent = (
      <div className={styles.pageHeaderContent}>
        <div className={styles.avatar}>
          <Avatar size="large" src={currentUser.avatar} />
        </div>
        <div className={styles.content}>
          <div className={styles.contentTitle}>
            Hi，
            {currentUser.name}
            ，祝你开心每一天！
          </div>
          <div>
            {currentUser.position ? currentUser.position : '职位'}
            <Divider type="vertical" />
            {currentUser.department ? currentUser.department : '部门'}
          </div>
        </div>
      </div>
    );
    const AvatarList = users.map(item => (
      <Tooltip key={item.username} title={item.name}>
        <Avatar
          alt={item.name}
          shape="square"
          size="large"
          src={item.avatar}
          className={styles.avatarList}
        />
      </Tooltip>
    ));
    const { visible } = this.state;
    return (
      <PageHeaderWrapper content={pageHeaderContent}>
        <Row gutter={24}>
          <Col xl={8} lg={24} md={24} sm={24} xs={24}>
            <Card
              bodyStyle={{ padding: 0 }}
              bordered={false}
              className={styles.activeCard}
              title="动态"
              loading={activitiesLoading}
            >
              <List loading={activitiesLoading} size="large">
                <div className={styles.activitiesList}>{this.renderActivities()}</div>
              </List>
            </Card>
          </Col>
          <Col xl={8} lg={24} md={24} sm={24} xs={24}>
            <Card
              bodyStyle={{ padding: 0 }}
              bordered={false}
              className={styles.activeCard}
              title="最近分享"
              loading={activitiesLoading}
            >
              <List loading={activitiesLoading} size="small">
                <div className={styles.activitiesList}>{this.renderBlogs()}</div>
              </List>
            </Card>
          </Col>
          <Col xl={8} lg={24} md={24} sm={24} xs={24}>
            <Card
              style={{ marginBottom: 24 }}
              title="便捷导航"
              bordered={false}
              bodyStyle={{ padding: 0 }}
            >
              <EditableLinkGroup
                onAdd={this.showModal}
                links={navLinks}
                linkElement="a"
                target="_blank"
              />
              <Modal
                title="快速添加"
                visible={visible}
                onOk={this.addLink}
                confirmLoading={addLinkLoading}
                onCancel={this.cancel}
                okText="提交"
              >
                <Form layout="vertical">
                  <FormItem>
                    {getFieldDecorator('title', {
                      rules: [
                        {
                          required: true,
                          message: '请输入导航名称!',
                        },
                      ],
                    })(<Input type="text" placeholder="导航名称" />)}
                  </FormItem>
                  <FormItem>
                    {getFieldDecorator('href', {
                      rules: [
                        {
                          required: true,
                          message: '请输入导航地址!',
                        },
                        {
                          type: 'url',
                          message: '导航地址格式不正确!',
                        },
                      ],
                    })(<Input type="text" placeholder="导航地址" />)}
                  </FormItem>
                </Form>
              </Modal>
            </Card>
            <Card style={{ marginBottom: 24 }} bordered={false} title="用户墙">
              <div>{AvatarList}</div>
            </Card>
          </Col>
        </Row>
      </PageHeaderWrapper>
    );
  }
}

export default Workplace;
