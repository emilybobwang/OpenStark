import React, { PureComponent } from 'react';
import { Form, Input, Button, Alert, Cascader, message, Upload, Icon, Row, Col } from 'antd';
import styles from '../../Dashboard/style.less';

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

export default class InfoForm extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      data: props.value,
      loading: false,
      imageUrl: props.value.avatar,
      value: '重发激活邮件',
      mailLoading: false,
      disabled: false,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('value' in nextProps) {
      this.setState({
        data: nextProps.value,
      });
    }
  }

  getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
  };

  beforeUpload = file => {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJPGorPNG) {
      message.error('请上传jpg或png格式的图片!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('图片大小必须小于2M!');
    }
    return isJPGorPNG && isLt2M;
  };

  handleChange = info => {
    if (info.file.status === 'uploading') {
      this.setState({ loading: true });
      return;
    }
    if (info.file.status === 'done') {
      this.getBase64(info.file.originFileObj, imageUrl =>
        this.setState({
          imageUrl,
          loading: false,
        })
      );
      if (info.file.response.status === 'SUCCESS') {
        message.success(info.file.response.message);
      } else {
        message.error(info.file.response.message);
      }
    } else if (info.file.status === 'error') {
      message.error('头像上传失败!');
      this.setState({
        loading: false,
      });
    }
  };

  sendActiveMail = () => {
    const { sendActiveMail } = this.props;
    this.setState({
      mailLoading: true,
    });
    sendActiveMail(()=>{
      const { editResult } = this.props;
      if (editResult && editResult.status === 'SUCCESS') {
        message.success(editResult.message);
        this.setState({
          value: '已发送',
          disabled: true,
        });
      } else {
        message.error(editResult && editResult.message);
      }
      this.setState({
        mailLoading: false,
      });
    });
  };

  handleSubmit = () => {
    const { saveCurrent, id } = this.props;
    const { data } = this.state;
    const saveData = data;
    if (!saveData.name || !saveData.username || !saveData.email || !saveData.department_id) {
      message.error('请填写完整的个人信息。');
    } else {
      saveCurrent({ type: id, data });
    }
  };

  handleFieldChange(e, fieldName) {
    const { data } = this.state;
    const newData = data;
    newData[fieldName] = e.target ? e.target.value : e;
    this.setState({
      data: { ...newData },
    });
  }

  renderMessage = (status, content) => {
    if (status === 'SUCCESS') {
      return <Alert style={{ marginBottom: 24 }} message={content} type="success" showIcon />;
    }
    return <Alert style={{ marginBottom: 24 }} message={content} type="error" showIcon />;
  };

  render() {
    const { loading, disabled, mailLoading, value, imageUrl, data } = this.state;
    const { departments, loading: proLoading, editResult } = this.props;
    const uploadButton = (
      <div>
        <Icon type={loading ? 'loading' : 'plus'} />
        <div>选择头像上传</div>
      </div>
    );
    const activeButton = (
      <Col>
        <Button
          style={{ color: 'rgba(0, 0, 0, 0.65)' }}
          onClick={this.sendActiveMail}
          disabled={disabled}
          loading={mailLoading}
        >
          {value}
        </Button>
      </Col>
    );
    const image = imageUrl;
    let status = '未激活';
    if (data.status === 0) {
      status = '禁用';
    }
    if (data.status === 2) {
      status = '正常';
    }

    return (
      <Form>
        <FormItem {...formItemLayout} label="头像">
          <Upload
            name="avatar"
            listType="picture-card"
            showUploadList={false}
            action="/api/py/upload/images/avatar"
            accept="image/png, image/jpeg"
            beforeUpload={this.beforeUpload}
            onChange={this.handleChange}
          >
            {image ? (
              <img src={image} alt="avatar" style={{ width: '128px', height: '128px' }} />
            ) : (
              uploadButton
            )}
          </Upload>
        </FormItem>
        <FormItem {...formItemLayout} label="用户名" required>
          <Input
            name="username"
            placeholder="用户名"
            className={styles.input}
            value={data.username}
            onChange={e => this.handleFieldChange(e, 'username')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="邮箱" required>
          <Input
            name="email"
            placeholder="邮箱"
            className={styles.input}
            value={data.email}
            onChange={e => this.handleFieldChange(e, 'email')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="姓名" required>
          <Input
            name="realname"
            placeholder="姓名"
            className={styles.input}
            value={data.realname}
            onChange={e => this.handleFieldChange(e, 'realname')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="工号">
          <Input
            name="workerId"
            placeholder="工号"
            className={styles.input}
            value={data.workerId}
            onChange={e => this.handleFieldChange(e, 'workerId')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="职位">
          <Input
            name="position"
            placeholder="职位"
            className={styles.input}
            value={data.position}
            onChange={e => this.handleFieldChange(e, 'position')}
          />
        </FormItem>
        <FormItem {...formItemLayout} label="部门" required>
          <Cascader
            defaultValue={data.department_id}
            options={departments}
            onChange={e => this.handleFieldChange(e, 'department_id')}
            placeholder="所属团队"
            style={{ width: '300px' }}
            changeOnSelect
          />
        </FormItem>
        <FormItem {...formItemLayout} label="角色">
          <Input
            placeholder="角色"
            className={styles.input}
            value={data.authority === 'admin' ? '管理员' : '普通用户'}
            style={{ color: 'rgba(0, 0, 0, 0.65)' }}
            disabled
          />
        </FormItem>
        <FormItem
          labelCol={{ sm: { span: 6 }, md: { span: 3 } }}
          wrapperCol={{ sm: { span: 18 }, md: { span: 18 }, lg: { span: 10 } }}
          label="状态"
        >
          <Row>
            <Col md={{ span: 16 }} xs={{ span: 10 }} sm={{ span: 18 }} lg={{ span: 17 }}>
              <Input
                placeholder="状态"
                className={styles.input}
                value={status}
                style={{ color: 'rgba(0, 0, 0, 0.65)' }}
                disabled
              />
            </Col>
            {data.status === 1 ? activeButton : ''}
          </Row>
        </FormItem>
        <FormItem {...formItemLayout} label="Token">
          <Input
            placeholder="Token"
            className={styles.input}
            value={data.token}
            style={{ color: 'rgba(0, 0, 0, 0.65)' }}
            disabled
          />
        </FormItem>
        <FormItem wrapperCol={{ sm: { offset: 6 }, md: { offset: 3 } }}>
          <Button
            loading={proLoading}
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
          !proLoading &&
          editResult.data.type === 'info' &&
          this.renderMessage(editResult.status, editResult.message)}
      </Form>
    );
  }
}
