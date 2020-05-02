import React, { Component } from 'react';
import { Form, Input, Button, Alert } from 'antd';
import { connect } from 'dva';
import styles from '../style.less';
import EnvView from './EnvView';

const FormItem = Form.Item;
const { TextArea } = Input;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/runShell'],
}))
@Form.create()
class ShellForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      shell: '',
      editShell: '',
      type: [],
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
      type: 'tools/getShell',
      payload: { id: params.id },
    });
  }

  componentWillReceiveProps(nextProps) {
    if ('tools' in nextProps && nextProps.tools.shell) {
      const value = nextProps.form.getFieldValue('env');
      const { type } = this.state;
      if (value && nextProps.tools.shell.type !== type) {
        value.detail = [];
      }
      const { shell } = nextProps.tools.shell;
      const {
        match: { params },
      } = nextProps;
      if (params.id !== '0') {
        this.setState({ shell });
      }
      this.setState({
        type: nextProps.tools.shell.type,
        testEnv: value,
      });
    }
  }

  validatorEnv = (rule, value, callback) => {
    const { server, detail } = value || { server: undefined, detail: [] };
    const { shell, editShell } = this.state;
    const {
      match: { params },
    } = this.props;
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    if (!detail || !detail.length) {
      callback('请选择具体服务器!');
    }
    if (params.id !== '0' ? !shell.trim() : !editShell.trim()) {
      callback('请填写SHELL脚本!');
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
        const { shell, editShell } = this.state;
        dispatch({
          type: 'tools/runShell',
          payload: {
            shell: params.id !== '0' ? shell : editShell,
            eid: values.env.server.key,
            ip: values.env.detail.map(item => item.key),
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
    const tValue = e && e.target ? e.target.value : e;
    this.setState({
      editShell: tValue,
    });
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
    const { shell, type, testEnv, editShell, display } = this.state;
    return (
      <div className={styles.baseView} ref={this.getViewDom}>
        <div className={styles.left}>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem label="测试环境:">
              {getFieldDecorator('env', {
                initialValue: testEnv,
                rules: [
                  {
                    validator: this.validatorEnv,
                  },
                ],
              })(<EnvView type={type} />)}
            </FormItem>
            <FormItem label="SHELL脚本:">
              <TextArea
                autoFocus
                value={params.id !== '0' ? shell : editShell}
                disabled={params.id !== '0'}
                onChange={this.handleFieldChange}
                style={{ width: 800, minHeight: 250 }}
                placeholder="请填写SHELL脚本"
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

export default ShellForm;
