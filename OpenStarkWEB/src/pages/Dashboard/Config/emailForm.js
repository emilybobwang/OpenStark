import React, { PureComponent } from 'react';
import { Form, Input, Button, Alert, Select } from 'antd';
import styles from '../style.less';

const { Option } = Select;
const FormItem = Form.Item;

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

export default class EmailForm extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      data: props.value,
    };
  }

  handleSubmit = () => {
    const { saveConfigs, id } = this.props;
    const { data } = this.state;
    const newData = data;
    saveConfigs({
      type: id,
      data: {
        emailHost: newData.emailHost,
        emailPort: newData.emailPort,
        emailUser: newData.emailUser,
        emailPasswd: newData.emailPasswd,
        emailSSL: newData.emailSSL,
        emailFrom: newData.emailFrom,
        emailType: newData.emailType,
      },
    });
  };

  sendTestMail = () => {
    const { saveConfigs, id } = this.props;
    const { data } = this.state;
    const newData = data;
    saveConfigs({
      type: id,
      data: {
        emailHost: newData.emailHost,
        emailPort: newData.emailPort,
        emailUser: newData.emailUser,
        emailPasswd: newData.emailPasswd,
        emailSSL: newData.emailSSL,
        emailFrom: newData.emailFrom,
        emailType: newData.emailType,
      },
      op: 'test',
    });
  };

  handleFieldChange(e, fieldName) {
    const { data } = this.state;
    const newData = data;
    newData[fieldName] = e.target ? e.target.value : e;
    this.setState({
      data: { ...newData },
    });
  }

  renderMessage = (res, content) => {
    if (res === 'SUCCESS') {
      return <Alert style={{ marginBottom: 24 }} message={content} type="success" showIcon />;
    }
    return <Alert style={{ marginBottom: 24 }} message={content} type="error" showIcon />;
  };

  render() {
    const { data } = this.state;
    const { loading, editResult } = this.props;
    return (
      <Form>
        <FormItem {...formItemLayout} label="服务器地址">
          <Input
            name="emailHost"
            placeholder="smtp.163.com"
            className={styles.input}
            value={data.emailHost}
            onChange={e => this.handleFieldChange(e, 'emailHost')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="协议端口">
          <Input
            name="emailPort"
            placeholder="465"
            type="number"
            min="0"
            className={styles.input}
            value={data.emailPort}
            onChange={e => this.handleFieldChange(e, 'emailPort')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="发件人显示为">
          <Input
            name="emailFrom"
            placeholder="someone@example.com"
            className={styles.input}
            value={data.emailFrom}
            onChange={e => this.handleFieldChange(e, 'emailFrom')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="登录账号">
          <Input
            name="emailUser"
            placeholder="MYWINDOMAIN\myusername 或 登录账号"
            className={styles.input}
            value={data.emailUser}
            onChange={e => this.handleFieldChange(e, 'emailUser')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="账号密码">
          <Input
            name="emailPasswd"
            placeholder="账号密码"
            type="password"
            className={styles.input}
            value={data.emailPasswd}
            onChange={e => this.handleFieldChange(e, 'emailPasswd')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="使用SSL登录">
          <Select
            name="emailSSL"
            value={data.emailSSL ? data.emailSSL : 'no'}
            onChange={e => this.handleFieldChange(e, 'emailSSL')}
            style={{ width: '150px' }}
          >
            <Option value="yes">是</Option>
            <Option value="no">否</Option>
          </Select>
        </FormItem>
        <FormItem {...formItemLayout} label="邮箱类型">
          <Select
            name="emailType"
            value={data.emailType ? data.emailType : 'normal'}
            onChange={e => this.handleFieldChange(e, 'emailType')}
            style={{ width: '150px' }}
          >
            <Option value="exchange">Exchange邮箱</Option>
            <Option value="normal">常规邮箱</Option>
          </Select>
        </FormItem>
        <FormItem wrapperCol={{ sm: { offset: 6 }, md: { offset: 3 } }}>
          <Button
            loading={loading}
            type="primary"
            htmlType="submit"
            style={{ width: '80px' }}
            onClick={this.handleSubmit}
            icon="save"
          >
            保存
          </Button>
          <Button
            onClick={this.sendTestMail}
            loading={loading}
            style={{ width: '150px', marginLeft: '50px' }}
            icon="mail"
          >
            发送测试邮件
          </Button>
        </FormItem>
        {editResult &&
          !loading &&
          editResult.data.type === 'email' &&
          this.renderMessage(editResult.status, editResult.message)}
      </Form>
    );
  }
}
