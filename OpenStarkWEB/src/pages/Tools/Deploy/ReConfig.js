import React, { Component } from 'react';
import { Form, Button, Alert, Card } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import EnvView from '../Shell/EnvView';

const FormItem = Form.Item;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/Reconfig'],
}))
@Form.create()
class ReConfig extends Component {
  constructor(props) {
    super(props);
    this.state = {
      display: 'none',
    };
  }

  validatorEnv = (rule, value, callback) => {
    const { server, detail, config } = value || {
      server: undefined,
      detail: [],
      config: undefined,
    };
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    if (!detail || !detail.length) {
      callback('请选择具体服务器!');
    }
    if (!config || !config.key) {
      callback('请选择要还原的配置文件!');
    }
    callback();
  };

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'tools/Reconfig',
          payload: {
            ip: values.reTarget.detail.map(item => item.key).toString(),
            filename: values.reTarget.config.key,
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

  render() {
    const {
      form: { getFieldDecorator },
      loading,
      tools: { runResult },
    } = this.props;
    const { display } = this.state;
    return (
      <PageHeaderWrapper>
        <Card>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem label="目标配置中心:" style={{ width: 800 }}>
              {getFieldDecorator('reTarget', {
                rules: [
                  {
                    validator: this.validatorEnv,
                  },
                ],
              })(<EnvView />)}
            </FormItem>
            <FormItem label="执行结果:" style={{ display }}>
              {runResult &&
                !loading &&
                this.renderMessage(
                  runResult.message,
                  runResult.status === 'SUCCESS' ? 'success' : 'error'
                )}
            </FormItem>
            <Button loading={loading} type="primary" icon="undo" htmlType="submit">
              开始还原
            </Button>
          </Form>
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default ReConfig;
