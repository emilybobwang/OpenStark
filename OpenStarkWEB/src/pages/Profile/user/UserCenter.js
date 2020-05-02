import React, { PureComponent, Fragment } from 'react';
import { connect } from 'dva';
import { Form, Card, Tabs, Alert, Input, Button, Popover, Progress } from 'antd';
import GridContent from '@/components/PageHeaderWrapper/GridContent';
import InfoForm from './infoForm';
import styles from '../../Dashboard/style.less';

const { TabPane } = Tabs;
const FormItem = Form.Item;

const passwordStatusMap = {
  ok: <div className={styles.success}>强度：强</div>,
  pass: <div className={styles.warning}>强度：中</div>,
  poor: <div className={styles.error}>强度：太短</div>,
};

const passwordProgressMap = {
  ok: 'success',
  pass: 'normal',
  poor: 'exception',
};

const formItemLayout = {
  labelCol: {
    sm: { span: 6 },
    md: { span: 3 },
  },
  wrapperCol: {
    sm: { span: 7 },
    md: { span: 4 },
  },
};

@connect(({ user, loading }) => ({
  user,
  departments: user.departments,
  submitting: loading.effects['user/editCurrent'],
}))
@Form.create()
class UserCenter extends PureComponent {
  state = {
    confirmDirty: false,
    visible: false,
    help: '',
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/getDepartments',
    });
    dispatch({
      type: 'user/fetchCurrent',
    });
  }

  getPasswordStatus = () => {
    const { form } = this.props;
    const value = form.getFieldValue('newPasswd');
    if (value && value.length > 9) {
      return 'ok';
    }
    if (value && value.length > 5) {
      return 'pass';
    }
    return 'poor';
  };

  hiddenPasswordProgress = () => {
    this.setState({
      visible: false,
    });
  };

  saveCurrent = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/editCurrent',
      payload: {
        ...data,
      },
    });
  };

  sendActiveMail = (callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/sendActiveMail',
      callback,
    });
  };

  handleSubmit = e => {
    const { form } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        const saveData = values;
        delete saveData.info;
        this.saveCurrent({ type: 'passwd', data: saveData });
      }
    });
  };

  checkConfirm = (rule, value, callback) => {
    const { form } = this.props;
    if (value && value !== form.getFieldValue('newPasswd')) {
      callback('两次输入的密码不匹配!');
    } else {
      callback();
    }
  };

  checkPassword = (rule, value, callback) => {
    const { visible, confirmDirty } = this.state;
    if (!value) {
      this.setState({
        help: '请输入密码！',
        visible: !!value,
      });
      callback('error');
    } else {
      this.setState({
        help: '',
      });
      if (!visible) {
        this.setState({
          visible: !!value,
        });
      }
      if (value.length < 6 || value.length > 20) {
        this.setState({
          help: '密码格式不对!',
        });
        callback('error');
      } else {
        const { form } = this.props;
        if (value && confirmDirty) {
          form.validateFields(['rePasswd'], { force: true });
        }
        callback();
      }
    }
  };

  renderPasswordProgress = () => {
    const { form } = this.props;
    const value = form.getFieldValue('newPasswd');
    const passwordStatus = this.getPasswordStatus();
    return value && value.length ? (
      <div className={styles[`progress-${passwordStatus}`]}>
        <Progress
          status={passwordProgressMap[passwordStatus]}
          className={styles.progress}
          strokeWidth={6}
          percent={value.length * 10 > 100 ? 100 : value.length * 10}
          showInfo={false}
        />
      </div>
    ) : null;
  };

  renderMessage = (status, content) => {
    if (status === 'SUCCESS') {
      return <Alert style={{ marginBottom: 24 }} message={content} type="success" showIcon />;
    }
    return <Alert style={{ marginBottom: 24 }} message={content} type="error" showIcon />;
  };

  render() {
    const {
      form,
      user: { currentUser, editResult },
      submitting,
      departments,
    } = this.props;
    const { help, visible } = this.state;
    const { getFieldDecorator } = form;
    return (
      <GridContent>
        <Fragment>
          <Card bordered={false}>
            <Tabs
              size="large"
              tabBarStyle={{ marginBottom: 24 }}
              onTabClick={this.hiddenPasswordProgress}
            >
              <TabPane tab="个人信息" key="info">
                {getFieldDecorator('info', {
                  initialValue: currentUser,
                })(
                  <InfoForm
                    editResult={editResult}
                    loading={submitting}
                    saveCurrent={this.saveCurrent}
                    departments={departments}
                    sendActiveMail={this.sendActiveMail}
                  />
                )}
              </TabPane>
              <TabPane tab="修改密码" key="passwd">
                <Form>
                  <FormItem {...formItemLayout} label="原密码">
                    {getFieldDecorator('password', {
                      rules: [
                        {
                          required: true,
                          message: '请输入原密码！',
                        },
                      ],
                    })(
                      <Input placeholder="请输入原密码" type="password" className={styles.input} />
                    )}
                  </FormItem>
                  <FormItem help={help} {...formItemLayout} label="新密码">
                    <Popover
                      content={
                        <div style={{ padding: '4px 0' }}>
                          {passwordStatusMap[this.getPasswordStatus()]}
                          {this.renderPasswordProgress()}
                          <div style={{ marginTop: 10 }}>
                            请输入 6-20 个字符。请不要使用容易被猜到的密码。
                          </div>
                        </div>
                      }
                      overlayStyle={{ width: 240 }}
                      placement="right"
                      visible={visible}
                    >
                      {getFieldDecorator('newPasswd', {
                        rules: [
                          {
                            required: true,
                            message: '请输入新密码！',
                          },
                          {
                            validator: this.checkPassword,
                          },
                        ],
                      })(
                        <Input
                          placeholder="6-20位密码，区分大小写"
                          type="password"
                          className={styles.input}
                        />
                      )}
                    </Popover>
                  </FormItem>
                  <FormItem {...formItemLayout} label="确认密码">
                    {getFieldDecorator('rePasswd', {
                      rules: [
                        {
                          required: true,
                          message: '请确认新密码！',
                        },
                        {
                          validator: this.checkConfirm,
                        },
                      ],
                    })(
                      <Input
                        placeholder="需要与新密码一致"
                        type="password"
                        className={styles.input}
                      />
                    )}
                  </FormItem>
                  <FormItem wrapperCol={{ sm: { offset: 6 }, md: { offset: 3 } }}>
                    <Button
                      loading={submitting}
                      type="primary"
                      htmlType="submit"
                      style={{ width: '80px' }}
                      onClick={this.handleSubmit}
                      icon="save"
                    >
                      保存
                    </Button>
                  </FormItem>
                  {editResult &&
                    !submitting &&
                    editResult.data.type === 'passwd' &&
                    this.renderMessage(editResult.status, editResult.message)}
                </Form>
              </TabPane>
            </Tabs>
          </Card>
        </Fragment>
      </GridContent>
    );
  }
}

export default UserCenter;
