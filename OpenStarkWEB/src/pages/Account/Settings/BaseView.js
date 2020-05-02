import React, { Component, Fragment } from 'react';
import { FormattedMessage } from 'umi/locale';
import { Form, Input, Upload, Button, Cascader, message, Row, Col } from 'antd';
import { connect } from 'dva';
import styles from '../../Tools/style.less';

const FormItem = Form.Item;

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

// 头像组件 方便以后独立，增加裁剪之类的功能
const AvatarView = ({ avatar, beforeUpload, handleChange, loading }) => (
  <Fragment>
    <div className={styles.avatar_title}>头像</div>
    <div className={styles.avatar}>
      <img src={avatar} alt="avatar" />
    </div>
    <Upload
      name="avatar"
      showUploadList={false}
      action="/api/py/upload/images/avatar"
      accept="image/png, image/jpeg"
      beforeUpload={beforeUpload}
      onChange={handleChange}
    >
      <div className={styles.button_view}>
        <Button icon="upload" loading={loading}>
          <FormattedMessage id="app.settings.basic.avatar" defaultMessage="Change avatar" />
        </Button>
      </div>
    </Upload>
  </Fragment>
);

@connect(({ user, loading }) => ({
  currentUser: user.currentUser,
  departments: user.departments,
  submitting: loading.effects['user/editCurrent'],
  loading: loading.effects['user/sendActiveMail'],
}))
@Form.create()
class BaseView extends Component {
  state = {
    loading: undefined,
    imageUrl: null,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/getDepartments',
    });
    dispatch({
      type: 'user/fetchCurrent',
    });
    this.setBaseInfo();
  }

  setBaseInfo = () => {
    const { currentUser, form } = this.props;
    Object.keys(form.getFieldsValue()).forEach(key => {
      const obj = {};
      if (key === 'status') {
        let status = '未激活';
        if (currentUser.status === 0) {
          status = '禁用';
        }
        if (currentUser.status === 2) {
          status = '正常';
        }
        obj[key] = status || '';
      } else if (key === 'authority') {
        obj[key] = currentUser.authority === 'admin' ? '管理员' : '普通用户' || '';
      } else {
        obj[key] = currentUser[key] || '';
      }
      form.setFieldsValue(obj);
    });
  };

  getAvatarURL() {
    const { currentUser } = this.props;
    const { imageUrl } = this.state;
    if (imageUrl) {
      return imageUrl;
    }
    if (currentUser.avatar) {
      return currentUser.avatar;
    }
    const url = 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png';
    return url;
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
            type: 'info',
            data: values,
          },
        });
      }
    });
  };

  sendActiveMail = () => {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/sendActiveMail',
    });
  };

  render() {
    const {
      form: { getFieldDecorator },
      departments,
      submitting,
      loading: mailLoading,
      currentUser,
    } = this.props;
    const { loading } = this.state;
    const activeButton = (
      <Col style={{ textAlign: 'right' }}>
        <Button
          icon="mail"
          style={{ color: 'rgba(0, 0, 0, 0.65)' }}
          onClick={this.sendActiveMail}
          loading={mailLoading}
        >
          重发激活邮件
        </Button>
      </Col>
    );
    return (
      <div className={styles.baseView} ref={this.getViewDom}>
        <div className={styles.left}>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem {...formItemLayout} label="用户名:" required>
              {getFieldDecorator('username', {
                rules: [
                  {
                    required: true,
                    message: '用户名不能为空!',
                  },
                ],
              })(<Input placeholder="用户名" />)}
            </FormItem>
            <FormItem {...formItemLayout} label="邮箱:" required>
              {getFieldDecorator('email', {
                rules: [
                  {
                    required: true,
                    message: '邮箱不能为空!',
                  },
                  {
                    type: 'email',
                    message: '邮箱格式不对!',
                  },
                ],
              })(<Input placeholder="邮箱" />)}
            </FormItem>
            <FormItem {...formItemLayout} label="姓名:" required>
              {getFieldDecorator('realname', {
                rules: [
                  {
                    required: true,
                    message: '姓名不能为空!',
                  },
                ],
              })(<Input placeholder="姓名" />)}
            </FormItem>
            <FormItem {...formItemLayout} label="工号:">
              {getFieldDecorator('workerId')(<Input placeholder="工号" />)}
            </FormItem>
            <FormItem {...formItemLayout} label="职位:">
              {getFieldDecorator('position')(<Input placeholder="职位" />)}
            </FormItem>
            <FormItem {...formItemLayout} label="部门:" required>
              {getFieldDecorator('department_id', {
                rules: [
                  {
                    required: true,
                    message: '部门不能为空!',
                  },
                ],
              })(
                <Cascader
                  options={departments}
                  placeholder="所属团队"
                  style={{ width: '300px' }}
                  changeOnSelect
                />
              )}
            </FormItem>
            <FormItem {...formItemLayout} label="角色:">
              {getFieldDecorator('authority')(
                <Input placeholder="角色" style={{ color: 'rgba(0, 0, 0, 0.65)' }} disabled />
              )}
            </FormItem>
            <FormItem {...formItemLayout} label="状态:">
              <Row style={{ width: 300 }}>
                <Col span={12}>
                  {getFieldDecorator('status')(
                    <Input
                      placeholder="状态"
                      style={{
                        color: 'rgba(0, 0, 0, 0.65)',
                        width: currentUser.status === 1 ? 150 : null,
                      }}
                      disabled
                    />
                  )}
                </Col>
                {currentUser.status === 1 ? activeButton : ''}
              </Row>
            </FormItem>
            <FormItem {...formItemLayout} label="Token:">
              {getFieldDecorator('token')(
                <Input placeholder="Token" style={{ color: 'rgba(0, 0, 0, 0.65)' }} disabled />
              )}
            </FormItem>
            <Button type="primary" loading={submitting} htmlType="submit">
              <FormattedMessage
                id="app.settings.basic.update"
                defaultMessage="Update Information"
              />
            </Button>
          </Form>
        </div>
        <div className={styles.right}>
          <AvatarView
            avatar={this.getAvatarURL()}
            beforeUpload={this.beforeUpload}
            handleChange={this.handleChange}
            loading={loading}
          />
        </div>
      </div>
    );
  }
}

export default BaseView;
