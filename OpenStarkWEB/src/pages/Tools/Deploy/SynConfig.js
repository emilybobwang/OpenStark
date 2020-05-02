import React, { Component } from 'react';
import { Form, Button, Alert, Card } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from '../style.less';
import EnvView from '../Shell/EnvView';

const FormItem = Form.Item;

@connect(({ tools, loading }) => ({
  tools,
  loading: loading.effects['tools/synConfig'],
}))
@Form.create()
class SynConfig extends Component {
  constructor(props) {
    super(props);
    this.state = {
      display: 'none',
    };
  }

  validatorEnv = (rule, value, callback) => {
    const { server, detail } = value || { server: undefined, detail: [] };
    if (!server || !server.key) {
      callback('请选择测试环境!');
    }
    if (!detail || !detail.length) {
      callback('请选择具体服务器!');
    }
    callback();
  };

  handleSubmit = e => {
    const { form, dispatch } = this.props;
    e.preventDefault();
    form.validateFields({ force: true }, (err, values) => {
      if (!err) {
        dispatch({
          type: 'tools/synConfig',
          payload: {
            sourceIp: values.source.detail.map(item => item.key).toString(),
            targetIp: values.target.detail.map(item => item.key).toString(),
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
            <FormItem label="源配置中心:">
              {getFieldDecorator('source', {
                rules: [
                  {
                    validator: this.validatorEnv,
                  },
                ],
              })(<EnvView />)}
            </FormItem>
            <FormItem label="目标配置中心:">
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
                  请大家慎重选择自己要同步的环境，不要替换错误，造成其他人不必要的工作量
                </p>
                <p style={{ color: 'red' }}>
                  同步配置中心主要功能是准生产的配置中心的内容同步到其他测试环境（需要保证测试环境web-9040是启动状态）
                </p>
                <p>
                  目前配置中心对6004-msg的发短信的已经改为86的挡板地址，如果需要发送真实短信，请将如下属性进行修改：
                </p>
                <p>1、sms.environment.dev=0</p>
                <p>2、sms.default.channel=itrigo</p>
                <p>3、sms.xw400.url=http://211.147.239.62:9050/cgi-bin/sendsms</p>
                <p>4、需要注释掉服务器hosts里面的 172.20.20.86 sdk4report.eucp.b2m.cn</p>
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
              开始同步
            </Button>
          </Form>
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default SynConfig;
