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

export default class CommonForm extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      data: props.value,
    };
  }

  componentWillReceiveProps(nextProps) {
    const { data } = this.state;
    if ('value' in nextProps && Object.keys(data).length === 0) {
      this.setState({
        data: nextProps.value,
      });
    }
  }

  handleSubmit = () => {
    const { saveConfigs, id } = this.props;
    const { data } = this.state;
    const newData = data;
    saveConfigs({
      type: id,
      data: {
        company: newData.company,
        sysName: newData.sysName,
        sysDesc: newData.sysDesc,
        emailExt: newData.emailExt,
        autoLogin: newData.autoLogin,
      },
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
        <FormItem {...formItemLayout} label="组织名称">
          <Input
            name="company"
            placeholder="鸥鹏斯塔克"
            className={styles.input}
            value={data.company}
            onChange={e => this.handleFieldChange(e, 'company')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="系统名称">
          <Input
            name="sysName"
            placeholder="斯塔克综合测试管理平台"
            className={styles.input}
            value={data.sysName}
            onChange={e => this.handleFieldChange(e, 'sysName')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="系统描述">
          <Input
            name="sysDesc"
            placeholder="让测试更高效 使测试更简单"
            className={styles.input}
            value={data.sysDesc}
            onChange={e => this.handleFieldChange(e, 'sysDesc')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="注册邮箱后缀">
          <Input
            name="emailExt"
            placeholder="openstark.com"
            className={styles.input}
            value={data.emailExt}
            onChange={e => this.handleFieldChange(e, 'emailExt')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="是否开启自动登录">
          <Select
            name="autoLogin"
            value={data.autoLogin ? data.autoLogin : 'no'}
            onChange={e => this.handleFieldChange(e, 'autoLogin')}
            style={{ width: '100px' }}
          >
            <Option value="yes">是</Option>
            <Option value="no">否</Option>
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
        </FormItem>
        {editResult &&
          !loading &&
          editResult.data.type === 'common' &&
          this.renderMessage(editResult.status, editResult.message)}
      </Form>
    );
  }
}
