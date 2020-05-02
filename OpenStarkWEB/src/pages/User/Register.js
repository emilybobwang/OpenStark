import React, { Component } from 'react';
import { connect } from 'dva';
import Link from 'umi/link';
import { Form, Input, Button, Popover, Progress, Cascader, Alert } from 'antd';
import styles from './Register.less';

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

@connect(({ register, user, global, loading }) => ({
  register,
  departments: user.departments,
  commonInfo: global.commonInfo,
  submitting: loading.effects['register/submit'],
}))
@Form.create()
class Register extends Component {
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
  }

  getPasswordStatus = () => {
    const { form } = this.props;
    const value = form.getFieldValue('password');
    if (value && value.length > 9) {
      return 'ok';
    }
    if (value && value.length > 5) {
      return 'pass';
    }
    return 'poor';
  };

  handleSubmit = e => {
    const { commonInfo, form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'register/submit',
          payload: {
            ...values,
            email: `${values.email}${commonInfo.emailExt}`,
          },
        });
      }
    });
  };

  handleConfirmBlur = e => {
    const { value } = e.target;
    const { confirmDirty } = this.state;
    this.setState({ confirmDirty: confirmDirty || !!value });
  };

  checkConfirm = (rule, value, callback) => {
    const { form } = this.props;
    if (value && value !== form.getFieldValue('password')) {
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
          form.validateFields(['confirm'], { force: true });
        }
        callback();
      }
    }
  };

  emailInput = () => {
    const { form, commonInfo } = this.props;
    const { getFieldDecorator } = form;
    if (commonInfo.emailExt) {
      return (
        <FormItem>
          {getFieldDecorator('email', {
            rules: [
              {
                required: true,
                message: '请输入邮箱地址！',
              },
              {
                type: 'string',
                message: '邮箱地址格式错误！',
              },
            ],
          })(<Input size="large" placeholder="邮箱" addonAfter={commonInfo.emailExt} autoFocus />)}
        </FormItem>
      );
    }
    return (
      <FormItem>
        {getFieldDecorator('email', {
          rules: [
            {
              required: true,
              message: '请输入邮箱地址！',
            },
            {
              type: 'email',
              message: '邮箱地址格式错误！',
            },
          ],
        })(<Input size="large" placeholder="邮箱" autoFocus />)}
      </FormItem>
    );
  };

  renderPasswordProgress = () => {
    const { form } = this.props;
    const value = form.getFieldValue('password');
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

  renderMessage = content => (
    <Alert style={{ marginBottom: 24 }} message={content} type="error" showIcon />
  );

  render() {
    const { form, register, submitting, departments } = this.props;
    const { getFieldDecorator } = form;
    const { help, visible } = this.state;
    return (
      <div className={styles.main}>
        <h3>注册</h3>
        {register.status === 'FAIL' && !register.submitting && this.renderMessage(register.message)}
        <Form onSubmit={this.handleSubmit}>
          {this.emailInput()}
          <FormItem>
            {getFieldDecorator('name', {
              rules: [
                {
                  required: true,
                  message: '请输入姓名！',
                },
                {
                  type: 'string',
                  message: '姓名格式错误！',
                },
              ],
            })(<Input size="large" placeholder="姓名" />)}
          </FormItem>
          <FormItem>
            {getFieldDecorator('department', {
              rules: [
                {
                  required: true,
                  type: 'array',
                  message: '请选择所属部门',
                },
              ],
            })(
              <Cascader options={departments} placeholder="所属部门" changeOnSelect size="large" />
            )}
          </FormItem>
          <FormItem help={help}>
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
              {getFieldDecorator('password', {
                rules: [
                  {
                    validator: this.checkPassword,
                  },
                ],
              })(<Input size="large" type="password" placeholder="6-20位密码，区分大小写" />)}
            </Popover>
          </FormItem>
          <FormItem>
            {getFieldDecorator('confirm', {
              rules: [
                {
                  required: true,
                  message: '请确认密码！',
                },
                {
                  validator: this.checkConfirm,
                },
              ],
            })(<Input size="large" type="password" placeholder="确认密码" />)}
          </FormItem>
          <FormItem>
            <Button
              size="large"
              loading={submitting}
              className={styles.submit}
              type="primary"
              htmlType="submit"
            >
              注册
            </Button>
            <Link className={styles.login} to="/user/login">
              使用已有账户登录
            </Link>
          </FormItem>
        </Form>
      </div>
    );
  }
}

export default Register;
