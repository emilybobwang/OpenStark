import React, { Component } from 'react';
import { Form, Button, Alert, Row, Col, Checkbox, Input, Card } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import EnvView from './EnvView';

const FormItem = Form.Item;
const { TextArea } = Input;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/syncDBs'],
}))
@Form.create()
class DiffDB extends Component {
  constructor(props) {
    super(props);
    this.state = {
      display: 'none',
      diffResult: undefined,
      doing: 'diff',
    };
  }

  componentDidMount(){
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/show',
      payload: undefined,
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('tools' in nextProps && nextProps.tools.runResult) {
      const {
        runResult: { data },
      } = nextProps.tools;
      if (typeof data === 'object') {
        this.setState({ diffResult: data });
      }
    }
  }

  validatorEnv = (rule, value, callback) => {
    const { server } = value || { server: undefined };
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    callback();
  };

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        this.setState({ display: '', diffResult: undefined, doing: 'diff' });
        dispatch({
          type: 'tools/syncDBs',
          op: 'diff',
          payload: {
            ...values,
          },
        });
      }
    });
  };

  execSQL = () => {
    const { dispatch } = this.props;
    const { diffResult } = this.state;
    this.setState({ doing: 'execSQL' });
    dispatch({
      type: 'tools/syncDBs',
      op: 'execSQL',
      payload: {
        path: diffResult && diffResult.path,
      },
    });
  };

  getViewDom = ref => {
    this.view = ref;
  };

  renderMessage = (content, error) => (
    <Alert style={{ marginBottom: 24 }} message={content} type={error} showIcon />
  );

  render() {
    const {
      form: { getFieldDecorator },
      loading,
      tools: { runResult },
    } = this.props;
    const { display, diffResult, doing } = this.state;
    return (
      <PageHeaderWrapper>
        <Card>
          <Row>
            <Col span={12}>
              <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
                <FormItem label="数据库:">
                  {getFieldDecorator('left', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(<EnvView />)}
                </FormItem>
                <FormItem label="参考数据库:">
                  {getFieldDecorator('right', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(<EnvView />)}
                </FormItem>
                <FormItem label="对比类型:" required>
                  {getFieldDecorator('objecType', {
                    initialValue: ['TABLE'],
                    rules: [
                      {
                        required: true,
                        message: '请选择对比类型!',
                      },
                    ],
                  })(
                    <Checkbox.Group>
                      <Row>
                        {[
                          'TABLE',
                          'VIEW',
                          'TRIGGER',
                          'PROCEDURE',
                          'FUNCTION',
                          'EVENT',
                          'GRANT',
                          'ALL',
                        ].map(item => (
                          <Col span={6} key={item}>
                            <Checkbox key={item} value={item}>
                              {item}
                              {item === 'ALL' ? ' (耗时较长)' : ''}
                            </Checkbox>
                          </Col>
                        ))}
                      </Row>
                    </Checkbox.Group>
                  )}
                </FormItem>
                <FormItem label="友情提示:">
                  <span>
                    <p style={{ color: 'red' }}>
                      请大家慎重选择自己要对比的环境，不要选择错误，造成其他人不必要的工作量，对比需要一定时间，请耐心等待！
                    </p>
                    <p>
                      可多选同时对比多个数据库，但此时只能对比所有的数据表，
                      <span style={{ color: 'red' }}>
                        留空则会对比所有的库(非常耗时，不建议这么做)
                      </span>
                      ，如果需要对比特定的数据表，请选择一个数据库进行操作。
                    </p>
                  </span>
                </FormItem>
                <FormItem label="执行结果:" style={{ display }}>
                  {runResult &&
                    !loading &&
                    this.renderMessage(
                      runResult.message,
                      runResult.status === 'SUCCESS' ? 'success' : 'error'
                    )}
                </FormItem>
                <Row>
                  <Col span={3}>
                    <Button
                      loading={loading && doing === 'diff'}
                      type="primary"
                      icon="swap"
                      htmlType="submit"
                      disabled={doing === 'execSQL' && loading}
                    >
                      {!(loading && doing === 'diff') ? '开始对比' : '对比中...请耐心等待...'}
                    </Button>
                  </Col>
                  <Col offset={18} style={{ textAlign: 'right' }}>
                    <Button
                      loading={diffResult && diffResult.content && loading && doing === 'execSQL'}
                      type="danger"
                      onClick={this.execSQL}
                      icon="import"
                      disabled={!(diffResult && diffResult.content) || loading}
                    >
                      {!(diffResult && diffResult.content && loading && doing === 'execSQL')
                        ? '执行SQL'
                        : '执行中...请耐心等待...'}
                    </Button>
                  </Col>
                </Row>
              </Form>
            </Col>
            <Col span={12} style={{ paddingLeft: 50 }}>
              <p>差异SQL</p>
              <TextArea
                value={diffResult && diffResult.content}
                style={{
                  backgroundColor: '#fff',
                  color: 'rgba(0, 0, 0, 0.65)',
                  minHeight: 470,
                  maxHeight: 600,
                  marginBottom: 30,
                }}
                placeholder="对比结果"
                disabled
              />
            </Col>
          </Row>
        </Card>
      </PageHeaderWrapper>
    );
  }
}
export default DiffDB;
