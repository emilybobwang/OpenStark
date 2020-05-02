import React, { PureComponent } from 'react';
import { connect } from 'dva';
import Link from 'umi/link';
import { Alert } from 'antd';
import Login from '@/components/Login';
import styles from './Login.less';

const { UserName, Password, Submit } = Login;

@connect(({ login, global, loading }) => ({
  login,
  commonInfo: global.commonInfo,
  submitting: loading.effects['login/login'],
}))
class LoginPage extends PureComponent {
  componentDidMount() {
    const {
      commonInfo: { autoLogin },
      dispatch,
    } = this.props;
    if (typeof autoLogin === 'undefined' || autoLogin) {
      dispatch({
        type: 'login/autoLogin',
      });
    }
  }

  handleSubmit = (err, values) => {
    if (!err) {
      const { dispatch } = this.props;
      dispatch({
        type: 'login/login',
        payload: {
          ...values,
        },
      });
    }
  };

  renderMessage = content => (
    <Alert style={{ marginBottom: 24 }} message={content} type="error" showIcon />
  );

  render() {
    const { login, submitting } = this.props;
    return (
      <div className={styles.main}>
        <Login
          onSubmit={this.handleSubmit}
          ref={form => {
            this.loginForm = form;
          }}
        >
          <h3 className={styles.title}>登录</h3>
          {login.status === 'FAIL' &&
            !login.submitting &&
            login.message &&
            this.renderMessage(login.message)}
          <UserName
            name="userName"
            placeholder="用户名或邮箱"
            onPressEnter={() => this.loginForm.validateFields(this.handleSubmit)}
            autoFocus
          />
          <Password
            name="password"
            placeholder="密码"
            onPressEnter={() => this.loginForm.validateFields(this.handleSubmit)}
          />
          <Submit loading={submitting}>登录</Submit>
          <div className={styles.other}>
            <Link style={{ float: 'left' }} to="">
              忘记密码
            </Link>
            <Link className={styles.register} to="/user/register">
              注册账户
            </Link>
          </div>
        </Login>
      </div>
    );
  }
}

export default LoginPage;
