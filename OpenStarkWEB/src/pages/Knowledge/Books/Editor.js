import React, { PureComponent, Fragment } from 'react';
import {
  Form,
  Input,
  Button,
  Cascader,
  Row,
  Col,
  Card,
  Icon,
  Divider,
  message,
  Select,
  Tooltip,
} from 'antd';
import { connect } from 'dva';
import Router, { goBack } from 'umi/router';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import ReactDOMServer from 'react-dom/server';
import ReactMarkdown from 'react-markdown';
import SimpleMDEEditor from 'yt-simplemde-editor';
import ReactNeditor from 'react-neditor';
// import BraftEditor, { EditorState } from 'braft-editor';
// import CodeHighlighter from 'braft-extensions/dist/code-highlighter';
// import 'prismjs/components/prism-java';
// import 'prismjs/components/prism-php';
// import 'prismjs/components/prism-python';
// import 'braft-editor/dist/index.css';
// import 'braft-extensions/dist/code-highlighter.css';
import styles from '../../Tools/style.less';

const FormItem = Form.Item;
const { Option } = Select;

@connect(({ knowledge, user, loading }) => ({
  currentUser: user.currentUser,
  knowledge,
  loading: loading.effects['knowledge/editBooks'],
  fetchLoading: loading.effects['knowledge/getBooks'],
}))
@Form.create()
class Editor extends PureComponent {
  state = {
    edType: 'md',
    // mediaItems: [],
    blog: '',
  };

  componentDidMount() {
    const {
      dispatch,
      match: { params },
    } = this.props;
    dispatch({
      type: 'knowledge/getBooks',
      op: 'cate',
      action: 'list',
    });
    if (params.key !== 'NEW_TEMP_KEY') {
      dispatch({
        type: 'knowledge/getBooks',
        op: 'book',
        action: 'single',
        payload: { bid: params.key },
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    if ('knowledge' in nextProps) {
      const {
        knowledge: { blogContent },
      } = nextProps;
      const { edType } = this.state;
      this.setState({
        // mediaItems,
        edType: blogContent.type || edType,
      });
    }
  }

  handleSubmit = e => {
    const {
      form,
      dispatch,
      match: { params },
    } = this.props;
    const { edType, blog } = this.state;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (edType === 'html' && blog === '') {
        return;
      }
      if (!err) {
        const cid = values.cid.length > 1 ? values.cid[1] : values.cid[0];
        dispatch({
          type: 'knowledge/editBooks',
          payload: {
            ...values,
            key: params.key,
            cid,
            blog: edType === 'html' ? blog : values.blog,
            type: edType,
          },
          op: 'book',
          action: 'edit',
          callback: () => {
            Router.push(
              `/knowledge/books/blog/${cid}/${params.key !== 'NEW_TEMP_KEY' ? params.key : 0}`
            );
          },
        });
      }
    });
  };

  // onChange = files => {
  //   const { mediaItems } = this.state;
  //   if (files.length < mediaItems.length) {
  //     const keys = [];
  //     let delKeys = [];
  //     files.forEach(item => {
  //       keys.push(item.id);
  //     });
  //     delKeys = mediaItems.filter(item => !keys.includes(item.id));
  //     const { dispatch } = this.props;
  //     dispatch({
  //       type: 'knowledge/rmMedias',
  //       payload: {
  //         keys: delKeys.map(item => item.id),
  //       },
  //     });
  //     this.setState({
  //       mediaItems: files.map(item => ({ id: item.id, type: item.type, url: item.url })),
  //     });
  //     dispatch({
  //       type: 'knowledge/getMedias',
  //     });
  //   }
  // };

  // beforeUpload = file => {
  //   const isLt5M = file.size / 1024 / 1024 <= 5;
  //   if (!isLt5M) {
  //     message.error('媒体文件必须小于5M!');
  //   }
  //   return isLt5M;
  // };

  // uploadFn = param => {
  //   const serverURL = '/api/py/upload/media/files';
  //   const xhr = new XMLHttpRequest();
  //   const fd = new FormData();
  //   const successFn = () => {
  //     // 假设服务端直接返回文件上传后的地址
  //     // 上传成功后调用param.success并传入上传后的文件地址
  //     param.success({
  //       url: xhr.response && JSON.parse(xhr.response).data,
  //       meta: {
  //         loop: true, // 指定音视频是否循环播放
  //         autoPlay: true, // 指定音视频是否自动播放
  //         controls: true, // 指定音视频是否显示控制栏
  //       },
  //     });
  //   };

  //   const progressFn = event => {
  //     // 上传进度发生变化时调用param.progress
  //     param.progress((event.loaded / event.total) * 100);
  //   };

  //   const errorFn = () => {
  //     // 上传发生错误时调用param.error
  //     param.error({
  //       msg: '媒体文件上传失败!',
  //     });
  //   };

  //   xhr.upload.addEventListener('progress', progressFn, false);
  //   xhr.addEventListener('load', successFn, false);
  //   xhr.addEventListener('error', errorFn, false);
  //   xhr.addEventListener('abort', errorFn, false);

  //   fd.append('files', param.file);
  //   xhr.open('POST', serverURL, true);
  //   xhr.send(fd);
  // };

  changeEditor = edType => {
    const {
      match: { params },
    } = this.props;
    if (params.key !== 'NEW_TEMP_KEY') {
      message.warn('编辑知识时不可切换编辑器!');
    } else {
      this.setState({ edType });
      message.success('编辑器切换成功, 原内容已自动保存, 刷新还原!');
    }
  };

  render() {
    const {
      form: { getFieldDecorator },
      fetchLoading,
      loading,
      knowledge: { bookCate, blogContent },
      currentUser,
      match: { params },
    } = this.props;
    const { edType, blog } = this.state;
    const options = bookCate.map(item => ({
      value: item.id,
      label: item.name,
      children: item.child.map(ele => ({ value: ele.id, label: ele.name })),
    }));
    // const hooks = {
    //   'open-braft-finder': () => {
    //     const { dispatch } = this.props;
    //     dispatch({
    //       type: 'knowledge/getMedias',
    //     });
    //   },
    // };

    // const edOptions = {
    //   includeEditors: ['blog'],
    //   syntaxs: [
    //     {
    //       name: 'JavaScript',
    //       syntax: 'javascript',
    //     },
    //     {
    //       name: 'HTML',
    //       syntax: 'html',
    //     },
    //     {
    //       name: 'CSS',
    //       syntax: 'css',
    //     },
    //     {
    //       name: 'Python',
    //       syntax: 'python',
    //     },
    //     {
    //       name: 'Java',
    //       syntax: 'java',
    //     },
    //     {
    //       name: 'PHP',
    //       syntax: 'php',
    //     },
    //   ],
    // };

    // BraftEditor.use(CodeHighlighter(edOptions));

    const editor =
      edType === 'md' ? (
        <FormItem required>
          <Tooltip
            defaultVisible
            placement="top"
            title="当前是Markdown编辑器模式, 使用切换编辑器按钮可切换到富文本编辑器"
          >
            {getFieldDecorator('blog', {
              initialValue: blogContent.blog || '',
              rules: [{ required: true, message: '请输入正文' }],
            })(
              <SimpleMDEEditor
                getMdeInstance={simplemde => {
                  this.simplemde = simplemde;
                }}
                options={{
                  spellChecker: false,
                  forceSync: true,
                  autosave: {
                    enabled: true,
                    delay: 5000,
                    uniqueId: 'article_content_'.concat(params.key),
                  },
                  renderingConfig: {
                    codeSyntaxHighlighting: true,
                  },
                  toolbar: [
                    'bold',
                    'italic',
                    'strikethrough',
                    'heading',
                    '|',
                    'quote',
                    'code',
                    'clean-block',
                    'table',
                    'horizontal-rule',
                    'unordered-list',
                    'ordered-list',
                    '|',
                    'link',
                    'image',
                    '|',
                    'side-by-side',
                    'fullscreen',
                    '|',
                    {
                      name: 'changeEditor',
                      action: () => {
                        this.changeEditor('html');
                      },
                      className: 'fa fa-edit',
                      title: '切换编辑器',
                    },
                  ],
                  previewRender(text) {
                    return ReactDOMServer.renderToString(
                      <ReactMarkdown
                        source={text}
                        className={styles.blogContent}
                        escapeHtml={false}
                      />
                    );
                  },
                }}
                uploadOptions={{
                  uploadUrl: '/api/py/upload/media/file',
                  jsonFieldName: 'data',
                }}
              />
            )}
          </Tooltip>
        </FormItem>
      ) : (
        <FormItem required validateStatus="error" help={blog === '' ? '请输入正文' : ''}>
          <ReactNeditor
            value={blogContent.blog}
            neditorPath="/neditor"
            onChange={value => {
              this.setState({ blog: value });
            }}
          />
          {/* {getFieldDecorator('blog', {
            initialValue: blogContent.blog,
              // ? EditorState.createFrom(blogContent.blog)
              // : EditorState.createFrom(''),
            validateTrigger: 'onBlur',
            rules: [
              {
                required: true,
                validator: (_, value, callback) => {
                  if (value.isEmpty()) {
                    callback('请输入正文');
                  } else {
                    callback();
                  }
                },
              },
            ],
          })(
            // <BraftEditor
            //   id="blog"
            //   style={{ border: '1px solid #d9d9d9' }}
            //   media={{
            //     items: mediaItems,
            //     uploadFn: this.uploadFn,
            //     validateFn: this.beforeUpload,
            //     onChange: this.onChange,
            //   }}
            //   hooks={hooks}
            //   placeholder="正文"
            // />
          )} */}
        </FormItem>
      );

    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false} loading={fetchLoading}>
            <Form onSubmit={this.handleSubmit} hideRequiredMark>
              <Row>
                <Col span={23}>
                  <Button type="primary" onClick={goBack}>
                    <Icon type="rollback" />
                    返回
                  </Button>
                </Col>
                <Col span={1}>
                  <Button type="primary" icon="save" loading={loading} htmlType="submit">
                    保存
                  </Button>
                </Col>
              </Row>
              <Divider />
              <Row>
                <Col span={14}>
                  <FormItem required>
                    {getFieldDecorator('title', {
                      initialValue: blogContent.title || '',
                      rules: [{ required: true, message: '请输入标题' }],
                    })(<Input autoFocus placeholder="标题" size="large" />)}
                  </FormItem>
                </Col>
                <Col offset={1} span={6}>
                  <FormItem required>
                    {getFieldDecorator('cid', {
                      initialValue: blogContent.cid || '',
                      rules: [
                        {
                          required: true,
                          type: 'array',
                          message: '请选择知识分类',
                        },
                      ],
                    })(<Cascader options={options} placeholder="知识分类" size="large" />)}
                  </FormItem>
                </Col>
                <Col offset={1} span={2}>
                  <FormItem required>
                    {getFieldDecorator('status', {
                      initialValue: blogContent.status || '1',
                      rules: [
                        {
                          required: true,
                          message: '请选择发布状态',
                        },
                      ],
                    })(
                      <Select placeholder="发布状态" size="large">
                        <Option value="1">公开</Option>
                        <Option value="0">私密</Option>
                      </Select>
                    )}
                  </FormItem>
                </Col>
              </Row>
              {editor}
              <FormItem required>
                {getFieldDecorator('uid', {
                  initialValue: blogContent.uid || currentUser.userId,
                })(<Input hidden />)}
              </FormItem>
              <FormItem required>
                {getFieldDecorator('author', {
                  initialValue: blogContent.author || currentUser.realname,
                })(<Input hidden />)}
              </FormItem>
            </Form>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Editor;
