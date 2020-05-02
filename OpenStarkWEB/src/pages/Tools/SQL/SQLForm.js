import React, { Component } from 'react';
import { Form, Input, Button, Alert } from 'antd';
import { connect } from 'dva';
import styles from '../style.less';
import EnvView from '../Shell/EnvView';

const FormItem = Form.Item;
const { TextArea } = Input;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/runSQL'],
}))
@Form.create()
class SQLForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sql: '',
      editSQL: '',
      type: '',
      dbName: '',
      testEnv: undefined,
      display: 'none',
    };
  }

  componentDidMount() {
    const {
      dispatch,
      match: { params },
    } = this.props;
    dispatch({
      type: 'tools/getSQL',
      payload: { id: params.id },
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('tools' in nextProps && nextProps.tools.sql) {
      const value = nextProps.form.getFieldValue('envSQL');
      const { type } = this.state;
      if (value && nextProps.tools.sql.type !== type) {
        value.detail = [];
      }
      const { sql, dbName, type: nType } = nextProps.tools.sql;
      const {
        match: { params },
      } = nextProps;
      if (params.id !== '0') {
        this.setState({ dbName, sql });
      }
      this.setState({
        type: nType,
        testEnv: value,
      });
    }
  }

  validatorEnv = (rule, value, callback) => {
    const { server, detail } = value || { server: undefined, detail: [] };
    const { sql, editSQL, dbName } = this.state;
    const {
      match: { params },
    } = this.props;
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    if (!detail || !detail.length) {
      callback('请选择具体服务器!');
    }
    if (!dbName || !dbName.trim()) {
      callback('请填写数据库名称!');
    }
    if (params.id !== '0' ? !sql.trim() : !editSQL.trim()) {
      callback('请填写SQL脚本!');
    }
    callback();
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
        const { sql, editSQL, dbName } = this.state;
        dispatch({
          type: 'tools/runSQL',
          payload: {
            sql: params.id !== '0' ? sql : editSQL,
            eid: values.envSQL.server.key,
            ip: values.envSQL.detail.map(item => item.key).toString(),
            db: dbName,
          },
        });
        this.setState({ display: '' });
      }
    });
  };

  getViewDom = ref => {
    this.view = ref;
  };

  handleFieldChange = e => {
    const tValue = e && e.target && e.target.value;
    const name = e && e.target && e.target.name;
    if (name === 'sql') {
      this.setState({
        editSQL: tValue,
      });
    } else if (name === 'dbName') {
      this.setState({
        dbName: tValue,
      });
    }
  };

  renderMessage = (content, error) => (
    <Alert style={{ marginBottom: 24 }} message={content} type={error} showIcon />
  );

  render() {
    const {
      form: { getFieldDecorator },
      loading,
      tools: { runResult },
      match: { params },
    } = this.props;
    const { sql, type, testEnv, editSQL, dbName, display } = this.state;
    return (
      <div className={styles.baseView} ref={this.getViewDom}>
        <div className={styles.left}>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem label="测试环境:">
              {getFieldDecorator('envSQL', {
                initialValue: testEnv,
                rules: [
                  {
                    validator: this.validatorEnv,
                  },
                ],
              })(<EnvView type={type} />)}
            </FormItem>
            <FormItem label="数据库名称:">
              <Input
                name="dbName"
                value={dbName}
                disabled={params.id !== '0'}
                onChange={this.handleFieldChange}
                placeholder="请填写数据库名称"
              />
            </FormItem>
            <FormItem label="SQL脚本:">
              <TextArea
                autoFocus
                name="sql"
                value={params.id !== '0' ? sql : editSQL}
                disabled={!['0', '10', '12'].includes(params.id)}
                onChange={this.handleFieldChange}
                style={{ width: 800, minHeight: 250 }}
                placeholder="请填写SQL脚本"
              />
            </FormItem>
            <FormItem label="执行结果:" style={{ display }}>
              {runResult &&
                !loading &&
                this.renderMessage(
                  runResult.message,
                  runResult.status === 'SUCCESS' ? 'success' : 'error'
                )}
            </FormItem>
            <Button loading={loading} type="primary" icon="enter" htmlType="submit">
              执行
            </Button>
          </Form>
        </div>
      </div>
    );
  }
}

export default SQLForm;
