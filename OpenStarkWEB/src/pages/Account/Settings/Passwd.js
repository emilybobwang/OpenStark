import React, { Component } from 'react';
import { Form, Input, Progress, Button, Popover } from 'antd';
import { connect } from 'dva';
import styles from '../../Tools/style.less';

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
    sm: { span: 8 },
    md: { span: 6 },
  },
  wrapperCol: {
    sm: { span: 16 },
    md: { span: 18 },
  },
};

@connect(({ loading }) => ({
  submitting: loading.effects['user/editCurrent'],
}))
@Form.create()
class Passwd extends Component {
  state = {
    confirmDirty: false,
    visible: false,
    help: '',
  };

  getViewDom = ref => {
    this.view = ref;
  };

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'user/editCurrent',
          payload: {
            type: 'passwd',
            data: values,
          },
        });
      }
    });
  };

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

  render() {
    const {
      form: { getFieldDecorator },
      submitting,
    } = this.props;
    const { help, visible } = this.state;
    return (
      <div className={styles.baseView} ref={this.getViewDom}>
        <div className={styles.left}>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem {...formItemLayout} label="原密码:" required>
              {getFieldDecorator('password', {
                rules: [
                  {
                    required: true,
                    message: '请输入原密码！',
                  },
                ],
              })(<Input placeholder="请输入原密码" type="password" className={styles.input} />)}
            </FormItem>
            <FormItem help={help} {...formItemLayout} label="新密码:" required>
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
            <FormItem {...formItemLayout} label="确认密码:" required>
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
              })(<Input placeholder="需要与新密码一致" type="password" className={styles.input} />)}
            </FormItem>
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
          </Form>
        </div>
      </div>
    );
  }
}

export default Passwd;
