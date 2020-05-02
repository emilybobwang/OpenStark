import React, { Component } from 'react';
import { Form, Button, Alert, Row, Col, Select, Tag, Input, Icon, message, Popconfirm, Card } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from '../style.less';
import EnvView from './EnvView';

const FormItem = Form.Item;
const { Option } = Select;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/syncDBs'],
}))
@Form.create()
class SyncDB extends Component {
  constructor(props) {
    super(props);
    this.state = {
      display: 'none',
      initDB: '',
      initTable: [],
      inputVisible: false,
      inputValue: '',
    };
  }

  componentWillReceiveProps(nextProps) {
    const { initDB } = this.state;
    if ('tools' in nextProps && initDB !== '') {
      this.setState({ initTable: nextProps.tools.initTable });
    }
  }

  onChange = value => {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/fetchDBs',
      op: 'init',
      payload: {
        db: value,
      },
    });
    this.setState({ initDB: value, inputVisible: false, inputValue: '' });
  };

  afterClose = removedTag => {
    const { initDB } = this.state;
    if (initDB === '') {
      message.error('请先选择初始化数据库!');
    } else {
      const { dispatch } = this.props;
      dispatch({
        type: 'tools/syncDBs',
        op: 'delInit',
        payload: {
          db: initDB,
          table: removedTag,
        },
        callback: ()=>{
          this.onChange(initDB);
        },
      });
    }
  };

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
        dispatch({
          type: 'tools/syncDBs',
          op: 'do',
          payload: {
            ...values,
          },
        });
        this.setState({ display: '' });
      }
    });
  };

  getViewDom = ref => {
    this.view = ref;
  };

  renderMessage = (content, error) => (
    <Alert style={{ marginBottom: 24 }} message={content} type={error} showIcon />
  );

  showInput = () => {
    this.setState({ inputVisible: true });
  };

  handleInputChange = e => {
    this.setState({ inputValue: e.target.value });
  };

  handleInputConfirm = () => {
    const { inputValue, initDB, initTable } = this.state;
    if (initDB === '') {
      message.error('请先选择初始化数据库!');
    } else if (initTable.indexOf(inputValue.trim()) !== -1 || inputValue.trim() === '') {
      message.error('初始化数据表已存在或为空!');
    } else {
      const { dispatch } = this.props;
      dispatch({
        type: 'tools/syncDBs',
        op: 'init',
        payload: {
          db: initDB,
          table: inputValue,
        },
        callback: ()=>{
          this.onChange(initDB);
        },
      });
    }
  };

  render() {
    const {
      form: { getFieldDecorator },
      loading,
      tools: { runResult, dbList },
    } = this.props;
    const { display, inputVisible, inputValue, initTable } = this.state;
    return (
      <PageHeaderWrapper>
        <Card>
          <Row>
            <Col span={14}>
              <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
                <FormItem label="源数据库:">
                  {getFieldDecorator('source', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(<EnvView />)}
                </FormItem>
                <FormItem label="目标数据库:">
                  {getFieldDecorator('target', {
                    rules: [
                      {
                        validator: this.validatorEnv,
                      },
                    ],
                  })(<EnvView />)}
                </FormItem>
                <FormItem label="友情提示:">
                  <span>
                    <p style={{ color: 'red' }}>
                      请大家慎重选择自己要同步的环境，不要选择错误，造成其他人不必要的工作量，同步需要一定时间，请耐心等待！
                    </p>
                    <p>
                      可多选同时同步多个数据库，但此时只能同步所有的数据表，留空则会同步所有的库，如果想同步特定的数据表，请选择一个数据库进行同步。
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
                <Button loading={loading} type="primary" icon="sync" htmlType="submit">
                  {!loading ? '开始同步' : '同步中...请耐心等待...'}
                </Button>
              </Form>
            </Col>
            <Col span={10}>
              <p>初始化数据表</p>
              <Row>
                <Col>
                  <Select
                    showSearch
                    placeholder="请选择数据库"
                    onChange={this.onChange}
                    style={{ width: 300, marginBottom: 30 }}
                  >
                    {dbList.map(item => (
                      <Option key={item.key} value={item.id} title={item.description}>
                        {item.title}
                      </Option>
                    ))}
                  </Select>
                </Col>
              </Row>
              <Row>
                <Col>
                  {initTable.map(item => (
                    <Popconfirm
                      placement="top"
                      title="确定要删除该初始化表?"
                      onConfirm={() => {
                        this.afterClose(item);
                      }}
                    >
                      <Tag style={{ marginBottom: 10 }} key={item}>
                        {item}
                      </Tag>
                    </Popconfirm>
                  ))}
                  {inputVisible && (
                    <Input
                      type="text"
                      size="small"
                      autoFocus
                      style={{ width: 100 }}
                      value={inputValue}
                      onChange={this.handleInputChange}
                      onBlur={this.handleInputConfirm}
                      onPressEnter={this.handleInputConfirm}
                    />
                  )}
                  {!inputVisible && (
                    <Tag
                      onClick={this.showInput}
                      style={{ background: '#fff', borderStyle: 'dashed' }}
                    >
                      <Icon type="plus" /> New Table
                    </Tag>
                  )}
                </Col>
              </Row>
            </Col>
          </Row>
        </Card>
      </PageHeaderWrapper>
    );
  }
}
export default SyncDB;
