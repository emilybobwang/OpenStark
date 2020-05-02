import React, { Component } from 'react';
import { Form, Button, Alert, Row, Col, Card, List, Popover } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import { parseDiff, Diff } from 'react-diff-view';
import './diffView.less';
import EnvView from './EnvView';

const FormItem = Form.Item;

@connect(({ tools, loading }) => ({
  runResult: tools.runResult,
  loading: loading.effects['tools/diffPackages'],
}))
@Form.create()
class DiffAPP extends Component {
  constructor(props) {
    super(props);
    this.state = {
      display: 'none',
      diffResult: undefined,
      sameValue: false,
      content: <p>loading...</p>,
    };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/show',
      payload: undefined,
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('runResult' in nextProps && nextProps.runResult) {
      const {
        runResult: { data },
      } = nextProps;
      if (typeof data === 'object') {
        this.setState({ diffResult: data });
      }
    }
  }

  validatorEnv = (rule, value, callback) => {
    const { form } = this.props;
    const { server, dbs, tables } = value || {
      server: undefined,
      dbs: undefined,
      tables: undefined,
    };
    const { server: appLeft } = form.getFieldValue('appLeft') || { server: undefined };
    const { server: appRight } = form.getFieldValue('appRight') || { server: undefined };
    const { field } = rule;
    const sameValue =
      (field === 'appLeft' && appRight && server && server.key === appRight.key) ||
      (field === 'appRight' && appLeft && server && server.key === appLeft.key);
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    if (field === 'appLeft' && (!dbs || !dbs.key)) {
      callback('请选择应用包!');
    }
    if (sameValue && (!tables || !tables.key)) {
      callback('请选择应用包版本!');
    }
    callback();
  };

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        this.setState({ display: '', diffResult: undefined });
        const { dbs } = values.appLeft;
        dispatch({
          type: 'tools/show',
          payload: undefined,
        });
        dispatch({
          type: 'tools/diffPackages',
          op: dbs.key.slice(0, 3),
          payload: {
            ...values,
          },
        });
      }
    });
  };

  onChange = (value, id) => {
    const { form } = this.props;
    const { server: appLeft } = form.getFieldValue('appLeft') || { server: undefined };
    const { server: appRight } = form.getFieldValue('appRight') || { server: undefined };
    const { server } = value;
    if (id === 'appLeft' && appRight && server && server.key === appRight.key) {
      this.setState({ sameValue: true });
    } else if (id === 'appRight' && appLeft && server && server.key === appLeft.key) {
      this.setState({ sameValue: true });
    } else {
      this.setState({ sameValue: false });
    }
  };

  getDiff = file => {
    const { dispatch } = this.props;
    this.setState({ content: <p>loading...</p> });
    dispatch({
      type: 'tools/getVers',
      op: 'content',
      payload: {
        file,
      },
      callback: res => {
        if (res.status === 'SUCCESS') {
          const files = parseDiff(res.data);
          const renderFile = ({ oldRevision, newRevision, type, hunks }) => (
            <Diff
              key={oldRevision.concat('-').concat(newRevision)}
              viewType="split"
              diffType={type}
              hunks={hunks}
            />
          );
          this.setState({
            content: (
              <div
                style={{
                  maxHeight: 800,
                  minWidth: '80vw',
                  overflow: 'hidden',
                  overflowY: 'auto',
                  border: '1px solid #d9d9d9',
                }}
              >
                {files.map(renderFile)}
              </div>
            ),
          });
        } else {
          this.setState({ content: <p>{res.message}</p> });
        }
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
      runResult,
    } = this.props;
    const { display, diffResult, sameValue, content } = this.state;
    return (
      <PageHeaderWrapper>
        <Card>
          <Row>
            <Col span={12}>
              <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
                <FormItem label="测试环境:">
                  {getFieldDecorator('appLeft', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(
                    <EnvView
                      onChange={e => this.onChange(e, 'appLeft')}
                      sameValue={sameValue}
                      version={diffResult && diffResult.leftVersion}
                    />
                  )}
                </FormItem>
                <FormItem label="参考环境:">
                  {getFieldDecorator('appRight', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(
                    <EnvView
                      onChange={e => this.onChange(e, 'appRight')}
                      sameValue={sameValue}
                      version={diffResult && diffResult.rightVersion}
                    />
                  )}
                </FormItem>
                <FormItem label="友情提示:">
                  <span>
                    <p style={{ color: 'red' }}>
                      请大家慎重选择自己要对比的环境，不要选择错误，造成其他人不必要的工作量，对比需要一定时间，请耐心等待！
                    </p>
                    <p>
                      当选择不同环境进行对比时，将对比所选应用包最近部署的版本在两个环境之间的差异。
                    </p>
                    <p>
                      当选择同一个环境进行对比时，需要选择应用包的版本，对比两个版本之间的差异。
                    </p>
                    <p style={{ color: 'red' }}>
                      当前仅对比应用包中 lib/xnol-应用名-app-版本号.jar
                      文件的差异，如有其他需求，请提供需要对比的jar包文件路径给专项组！
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
                  <Button
                    loading={loading}
                    type="primary"
                    icon="swap"
                    htmlType="submit"
                    disabled={loading}
                  >
                    {!loading ? '开始对比' : '对比中...请耐心等待...'}
                  </Button>
                </Row>
              </Form>
            </Col>
            <Col span={12} style={{ paddingLeft: 50 }}>
              <p>差异文件列表</p>
              <div
                style={{ overflowY: 'auto', overflowX: 'hidden', minHeight: 500, maxHeight: 800 }}
              >
                <List
                  size="small"
                  bordered
                  dataSource={diffResult && diffResult.diffRes}
                  renderItem={item => (
                    <List.Item>
                      <Popover title={item.key} content={content} trigger="click">
                        <a onClick={() => this.getDiff(item.file)}>{item.title}</a>
                      </Popover>
                    </List.Item>
                  )}
                />
              </div>
            </Col>
          </Row>
        </Card>
      </PageHeaderWrapper>
    );
  }
}
export default DiffAPP;
