import React, { Component } from 'react';
import { Form, Button, Alert, DatePicker, Card } from 'antd';
import { connect } from 'dva';
import moment from 'moment';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import EnvView from './EnvView';

const FormItem = Form.Item;

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
    };
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
        dispatch({
          type: 'tools/syncDBs',
          op: 'recover',
          payload: {
            ...values,
            date: values.date.format('YYYYMMDD'),
          },
        });
        this.setState({ display: '' });
      }
    });
  };

  onChange = value => {
    const { dispatch, form } = this.props;
    const { server } = form.getFieldValue('reTarget') || { server: undefined };
    dispatch({
      type: 'tools/fetchDBs',
      op: 'db',
      payload: {
        key: server && server.key,
        date: value.format('YYYYMMDD'),
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
      form: { getFieldDecorator, getFieldValue },
      loading,
      tools: { runResult },
    } = this.props;
    const { display } = this.state;
    return (
      <PageHeaderWrapper>
        <Card>
          <Form layout="vertical" onSubmit={this.handleSubmit} hideRequiredMark>
            <FormItem label="还原到:">
              {getFieldDecorator('date', {
                initialValue: moment(new Date(), 'YYYY-MM-DD'),
                rules: [
                  {
                    validator: (_, value, callback) => {
                      if (!value) {
                        callback('请选择日期!');
                      } else {
                        callback();
                      }
                    },
                  },
                ],
              })(
                <DatePicker
                  allowClear={false}
                  format="YYYY-MM-DD"
                  placeholder="请选择需要还原到哪一天"
                  onChange={this.onChange}
                />
              )}
            </FormItem>
            <FormItem label="目标数据库:">
              {getFieldDecorator('reTarget', {
                rules: [
                  {
                    validator: this.validatorEnv,
                  },
                ],
              })(<EnvView date={getFieldValue('date').format('YYYYMMDD')} />)}
            </FormItem>
            <FormItem label="友情提示:">
              <span>
                <p style={{ color: 'red' }}>
                  还原后的数据库也是空库，不能恢复数据，请慎重操作，仅能还原一个月以内的备份，还原需要一定时间，请耐心等待！
                </p>
                <p>
                  可多选同时还原多个数据库，留空则还原所选日期的全部备份库，还原会恢复所有的表结构，不能指定表，请慎重操作。
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
            <Button loading={loading} type="primary" icon="undo" htmlType="submit">
              {!loading ? '开始还原' : '还原中...请耐心等待...'}
            </Button>
          </Form>
        </Card>
      </PageHeaderWrapper>
    );
  }
}
export default SyncDB;
