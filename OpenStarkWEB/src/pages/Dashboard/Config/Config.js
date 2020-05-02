import React, { PureComponent, Fragment } from 'react';
import { connect } from 'dva';
import { Form, Card, Tabs } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import CommonForm from './commonForm';
import EmailForm from './emailForm';
import NavForm from './navForm';

const { TabPane } = Tabs;

@connect(({ config, loading }) => ({
  config,
  submitting: loading.effects['config/editConfig'],
}))
@Form.create()
class Config extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'config/fetchConfig',
    });
  }

  saveConfigs = (data, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'config/editConfig',
      payload: {
        ...data,
      },
      callback,
    });
  };

  render() {
    const {
      form,
      config: { configs, editResult },
      submitting,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            <Tabs size="large" tabBarStyle={{ marginBottom: 24 }}>
              <TabPane tab="通用配置" key="common">
                {getFieldDecorator('common', {
                  initialValue: configs,
                })(
                  <CommonForm
                    editResult={editResult}
                    loading={submitting}
                    saveConfigs={this.saveConfigs}
                  />
                )}
              </TabPane>
              <TabPane tab="系统邮箱配置" key="email">
                {getFieldDecorator('email', {
                  initialValue: configs,
                })(
                  <EmailForm
                    editResult={editResult}
                    loading={submitting}
                    saveConfigs={this.saveConfigs}
                  />
                )}
              </TabPane>
              <TabPane tab="公共便捷导航管理" key="navLink">
                {getFieldDecorator('navLink', {
                  initialValue: configs.navLink ? configs.navLink : [],
                })(
                  <NavForm
                    editStatus={editResult}
                    loading={submitting}
                    saveRow={this.saveConfigs}
                    removeRow={this.saveConfigs}
                  />
                )}
              </TabPane>
            </Tabs>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Config;
