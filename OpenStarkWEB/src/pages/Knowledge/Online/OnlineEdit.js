import React, { PureComponent, Fragment } from 'react';
import {
  Form,
  Input,
  Button,
  message,
  Row,
  Col,
  Card,
  DatePicker,
  Select,
  Icon,
  Divider,
} from 'antd';
import { connect } from 'dva';
import Router, { goBack } from 'umi/router';
import moment from 'moment';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import BraftEditor, { EditorState } from 'braft-editor';
import 'braft-editor/dist/index.css';

const { TextArea } = Input;
const { Option } = Select;

const FormItem = Form.Item;

const formItemLayout = {
  labelCol: {
    sm: { span: 6 },
    md: { span: 4 },
  },
  wrapperCol: {
    sm: { span: 16 },
    md: { span: 18 },
  },
};

@connect(({ knowledge, project, loading }) => ({
  knowledge,
  teams: project.teams,
  loading: loading.effects['knowledge/editBooks'],
  searchLoading: loading.effects['knowledge/getOnline'],
}))
@Form.create()
class OnlineEdit extends PureComponent {
  state = {
    values: {},
    mediaItems: [],
  };

  componentDidMount() {
    const {
      dispatch,
      match: { params },
    } = this.props;
    dispatch({
      type: 'knowledge/getOnline',
      op: 'online',
      action: 'list',
      payload: {
        key: params.key,
      },
    });
    dispatch({
      type: 'project/fetchTeams',
      payload: {
        type: 'teams',
      },
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('knowledge' in nextProps) {
      const {
        knowledge: { online, mediaItems },
        form,
      } = nextProps;
      this.setState({ mediaItems });
      if (Array.isArray(online.data) && online.data.length > 0) {
        const obj = {};
        Object.keys(form.getFieldsValue()).forEach(key => {
          if (['foundTime', 'publishTime', 'analyzeTime', 'closeTime'].includes(key)) {
            obj[key] =
              (online.data[0][key] && moment(online.data[0][key], 'YYYY-MM-DD')) ||
              moment(new Date(), 'YYYY-MM-DD');
          } else if (['bug', 'cause', 'answer'].includes(key)) {
            obj[key] =
              online.data[0][key] &&
              EditorState.createFrom(online.data[0][key] || EditorState.createFrom(''));
          } else {
            obj[key] = online.data[0][key] || '';
          }
        });
        this.setState({ values: obj });
      }
    }
  }

  onChange = files => {
    const { mediaItems } = this.state;
    if (files.length < mediaItems.length) {
      const keys = [];
      let delKeys = [];
      files.forEach(item => {
        keys.push(item.id);
      });
      delKeys = mediaItems.filter(item => !keys.includes(item.id));
      const { dispatch } = this.props;
      dispatch({
        type: 'knowledge/rmMedias',
        payload: {
          keys: delKeys.map(item => item.id),
        },
      });
      this.setState({
        mediaItems: files.map(item => ({ id: item.id, type: item.type, url: item.url })),
      });
      dispatch({
        type: 'knowledge/getMedias',
      });
    }
  };

  beforeUpload = file => {
    const isLt5M = file.size / 1024 / 1024 <= 5;
    if (!isLt5M) {
      message.error('媒体文件必须小于5M!');
    }
    return isLt5M;
  };

  uploadFn = param => {
    const serverURL = '/api/py/upload/media/files';
    const xhr = new XMLHttpRequest();
    const fd = new FormData();
    const successFn = () => {
      // 假设服务端直接返回文件上传后的地址
      // 上传成功后调用param.success并传入上传后的文件地址
      param.success({
        url: xhr.response && JSON.parse(xhr.response).data,
        meta: {
          loop: true, // 指定音视频是否循环播放
          autoPlay: true, // 指定音视频是否自动播放
          controls: true, // 指定音视频是否显示控制栏
        },
      });
    };

    const progressFn = event => {
      // 上传进度发生变化时调用param.progress
      param.progress((event.loaded / event.total) * 100);
    };

    const errorFn = () => {
      // 上传发生错误时调用param.error
      param.error({
        msg: '媒体文件上传失败!',
      });
    };

    xhr.upload.addEventListener('progress', progressFn, false);
    xhr.addEventListener('load', successFn, false);
    xhr.addEventListener('error', errorFn, false);
    xhr.addEventListener('abort', errorFn, false);

    fd.append('files', param.file);
    xhr.open('POST', serverURL, true);
    xhr.send(fd);
  };

  handleSubmit = e => {
    const {
      form,
      dispatch,
      match: { params },
    } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'knowledge/editBooks',
          payload: {
            ...values,
            key: params.key,
            bug: values.bug.toRAW(true),
            cause: values.cause.toRAW(true),
            answer: values.answer.toRAW(true),
            foundTime: values.foundTime.format('YYYY-MM-DD'),
            publishTime: values.publishTime.format('YYYY-MM-DD'),
            analyzeTime: values.analyzeTime.format('YYYY-MM-DD'),
            closeTime: values.closeTime.format('YYYY-MM-DD'),
          },
          op: 'online',
          action: 'edit',
          callback: ()=>{
            Router.push('/knowledge/online');
          },
        });
      }
    });
  };

  render() {
    const {
      form: { getFieldDecorator },
      teams,
      searchLoading,
      loading,
    } = this.props;
    const { values, mediaItems } = this.state;
    const hooks = {
      'open-braft-finder': () => {
        const { dispatch } = this.props;
        dispatch({
          type: 'knowledge/getMedias',
        });
      },
    };
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false} loading={searchLoading}>
            <Row>
              <Col span={24}>
                <Button type="primary" onClick={goBack}>
                  <Icon type="rollback" />
                  返回
                </Button>
              </Col>
            </Row>
            <Divider />
            <Form onSubmit={this.handleSubmit} hideRequiredMark>
              <FormItem {...formItemLayout} label="发现日期:" required>
                {getFieldDecorator('foundTime', {
                  initialValue: values.foundTime || moment(new Date(), 'YYYY-MM-DD'),
                  rules: [
                    {
                      required: true,
                      message: '发现日期不能为空!',
                    },
                  ],
                })(
                  <DatePicker
                    allowClear={false}
                    format="YYYY-MM-DD"
                    placeholder="发现日期"
                    style={{ width: 200 }}
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="所属组:" required>
                {getFieldDecorator('tid', {
                  initialValue: values.tid,
                  rules: [
                    {
                      required: true,
                      message: '所属组不能为空!',
                    },
                  ],
                })(
                  <Select placeholder="所属组" style={{ width: 200 }}>
                    {teams.map(item => (
                      <Option key={item.tid} value={item.tid}>
                        {item.name}
                      </Option>
                    ))}
                  </Select>
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="严重程度:" required>
                {getFieldDecorator('severity', {
                  initialValue: values.severity,
                  rules: [
                    {
                      required: true,
                      message: '严重程度不能为空!',
                    },
                  ],
                })(
                  <Select style={{ width: 200 }} placeholder="严重程度">
                    {['提示', '轻微', '一般', '严重', '致命'].map(item => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="功能模块:">
                {getFieldDecorator('module', {
                  initialValue: values.module,
                })(<Input autoFocus placeholder="功能模块" />)}
              </FormItem>
              <FormItem {...formItemLayout} label="对应需求:">
                {getFieldDecorator('requirement', {
                  initialValue: values.requirement,
                })(<TextArea placeholder="对应需求" />)}
              </FormItem>
              <FormItem {...formItemLayout} label="发布日期:" required>
                {getFieldDecorator('publishTime', {
                  initialValue: values.publishTime || moment(new Date(), 'YYYY-MM-DD'),
                  rules: [
                    {
                      required: true,
                      message: '发布日期不能为空!',
                    },
                  ],
                })(
                  <DatePicker
                    allowClear={false}
                    format="YYYY-MM-DD"
                    placeholder="发布日期"
                    style={{ width: 200 }}
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="责任人:" required>
                {getFieldDecorator('principal', {
                  initialValue: values.principal,
                  rules: [
                    {
                      required: true,
                      message: '责任人不能为空!',
                    },
                  ],
                })(<Input placeholder="责任人" />)}
              </FormItem>
              <FormItem {...formItemLayout} label="线上bug描述:" required>
                {getFieldDecorator('bug', {
                  initialValue: values.bug,
                  validateTrigger: 'onBlur',
                  rules: [
                    {
                      required: true,
                      validator: (_, value, callback) => {
                        if (value.isEmpty()) {
                          callback('线上bug描述不能为空');
                        } else {
                          callback();
                        }
                      },
                    },
                  ],
                })(
                  <BraftEditor
                    style={{ border: '1px solid #d9d9d9' }}
                    media={{
                      items: mediaItems,
                      uploadFn: this.uploadFn,
                      validateFn: this.beforeUpload,
                      onChange: this.onChange,
                    }}
                    hooks={hooks}
                    placeholder="线上bug描述"
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="问题影响:">
                {getFieldDecorator('effect', {
                  initialValue: values.effect,
                })(<TextArea placeholder="问题影响" />)}
              </FormItem>
              <FormItem {...formItemLayout} label="问题处理:">
                {getFieldDecorator('solution', {
                  initialValue: values.solution,
                })(<TextArea placeholder="问题处理" />)}
              </FormItem>
              <FormItem {...formItemLayout} label="缺陷归属:" required>
                {getFieldDecorator('attribution', {
                  initialValue: values.attribution,
                  rules: [
                    {
                      required: true,
                      message: '缺陷归属不能为空!',
                    },
                  ],
                })(
                  <Select style={{ width: 200 }} placeholder="缺陷归属">
                    {[
                      '回归测试遗漏',
                      '测试数据准备不足引起',
                      '需求遗漏',
                      '产品设计不合理',
                      '开发问题',
                      '框架设计问题',
                      '无线上环境验证引起',
                      '用户体验',
                      '其他',
                    ].map(item => (
                      <Option key={item} value={item}>
                        {item}
                      </Option>
                    ))}
                  </Select>
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="原因分析:" required>
                {getFieldDecorator('cause', {
                  initialValue: values.cause,
                  validateTrigger: 'onBlur',
                  rules: [
                    {
                      required: true,
                      validator: (_, value, callback) => {
                        if (value.isEmpty()) {
                          callback('原因分析不能为空');
                        } else {
                          callback();
                        }
                      },
                    },
                  ],
                })(
                  <BraftEditor
                    style={{ border: '1px solid #d9d9d9' }}
                    media={{
                      items: mediaItems,
                      uploadFn: this.uploadFn,
                      validateFn: this.beforeUpload,
                      onChange: this.onChange,
                    }}
                    hooks={hooks}
                    placeholder="原因分析"
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="测试规避措施:" required>
                {getFieldDecorator('answer', {
                  initialValue: values.answer,
                  validateTrigger: 'onBlur',
                  rules: [
                    {
                      required: true,
                      validator: (_, value, callback) => {
                        if (value.isEmpty()) {
                          callback('测试规避措施不能为空');
                        } else {
                          callback();
                        }
                      },
                    },
                  ],
                })(
                  <BraftEditor
                    style={{ border: '1px solid #d9d9d9' }}
                    media={{
                      items: mediaItems,
                      uploadFn: this.uploadFn,
                      validateFn: this.beforeUpload,
                      onChange: this.onChange,
                    }}
                    hooks={hooks}
                    placeholder="测试规避措施"
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="分析日期:" required>
                {getFieldDecorator('analyzeTime', {
                  initialValue: values.analyzeTime || moment(new Date(), 'YYYY-MM-DD'),
                  rules: [
                    {
                      required: true,
                      message: '分析日期不能为空!',
                    },
                  ],
                })(
                  <DatePicker
                    allowClear={false}
                    format="YYYY-MM-DD"
                    placeholder="分析日期"
                    style={{ width: 200 }}
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="状态:" required>
                {getFieldDecorator('status', {
                  initialValue: (values.status && values.status.toString()) || '1',
                  rules: [
                    {
                      required: true,
                      message: '状态不能为空!',
                    },
                  ],
                })(
                  <Select placeholder="状态" style={{ width: 200 }}>
                    <Option value="1">打开</Option>
                    <Option value="0">关闭</Option>
                  </Select>
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="关闭日期:">
                {getFieldDecorator('closeTime', {
                  initialValue: values.closeTime || moment(new Date(), 'YYYY-MM-DD'),
                })(
                  <DatePicker
                    allowClear={false}
                    format="YYYY-MM-DD"
                    placeholder="关闭日期"
                    style={{ width: 200 }}
                  />
                )}
              </FormItem>
              <FormItem {...formItemLayout} label="备注:">
                {getFieldDecorator('remarks', {
                  initialValue: values.remarks,
                })(<TextArea placeholder="备注" />)}
              </FormItem>
              <Row>
                <Col sm={{ offset: 6 }} md={{ offset: 4 }}>
                  <Button type="primary" icon="save" loading={loading} htmlType="submit">
                    保存
                  </Button>
                </Col>
              </Row>
            </Form>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default OnlineEdit;
