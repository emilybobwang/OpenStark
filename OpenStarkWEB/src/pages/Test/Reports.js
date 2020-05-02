import React, { PureComponent, Fragment } from 'react';
import { Card, Tabs } from 'antd';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import JacocoReportsForm from './reportsForm';

const { TabPane } = Tabs;

class JacocoReports extends PureComponent {
  render() {
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            <Tabs tabBarStyle={{ marginBottom: 24 }}>
              <TabPane tab="JaCoCo覆盖率测试报告" key="jacoco">
                <JacocoReportsForm {...this.props} />
              </TabPane>
            </Tabs>
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default JacocoReports;
