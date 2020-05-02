import React, { PureComponent, Fragment } from 'react';
import { Card, Form, Tabs } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import ReportsForm from './reportsForm';
import JacocoReportsForm from '../../Test/reportsForm';

const { TabPane } = Tabs;

@connect(({ user, guiTest, project, loading }) => ({
  guiTest,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['guiTest/editGuiTest'],
  searchLoading: loading.effects['guiTest/fetchGuiReports'],
}))
@Form.create()
class Reports extends PureComponent {
  componentDidMount() {
    const {
      dispatch,
      match: { url },
    } = this.props;
    dispatch({
      type: 'jobs/fetchReports',
      op: 'jacoco',
      payload: {
        type: url.split('/')[1],
      },
    });
    dispatch({
      type: 'guiTest/fetchGuiReports',
      op: 'reports',
      action: 'list',
    });
    dispatch({
      type: 'project/fetchProjects',
      payload: {
        type: 'projects',
      },
    });
    dispatch({
      type: 'project/fetchTeams',
      payload: {
        type: 'teams',
      },
    });
  }

  onSearch = filters => {
    const {
      guiTest: { reportsList },
      dispatch,
    } = this.props;
    dispatch({
      type: 'guiTest/fetchGuiReports',
      payload: {
        size: reportsList.size,
        ...filters,
      },
      op: 'reports',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'guiTest/editGuiTest',
      payload: {
        ...data,
      },
      op: 'reports',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      guiTest: { reportsList, editResult },
      project,
      loading,
      searchLoading,
      currentUser,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            <Tabs tabBarStyle={{ marginBottom: 24 }}>
              <TabPane tab="GUI自动化测试报告" key="reports">
                {getFieldDecorator('reports', {
                  initialValue: reportsList.data,
                })(
                  <ReportsForm
                    loading={loading || searchLoading}
                    editStatus={editResult}
                    onSearch={this.onSearch}
                    editRows={this.editRows}
                    reportsList={reportsList}
                    project={project}
                    currentUser={currentUser}
                  />
                )}
              </TabPane>
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

export default Reports;
