import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import JobsForm from './jobsForm';

@connect(({ user, guiTest, project, loading }) => ({
  guiTest,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['guiTest/editGuiTest'],
  searchLoading: loading.effects['guiTest/fetchGuiJobs'],
}))
@Form.create()
class Jobs extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
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
    dispatch({
      type: 'guiTest/fetchGuiJobs',
      op: 'jobs',
      action: 'list',
      payload: {
        test_type: 'job',
      },
    });
  }

  onSearch = filters => {
    const {
      guiTest: { jobsList },
      dispatch,
    } = this.props;
    dispatch({
      type: 'guiTest/fetchGuiJobs',
      payload: {
        size: jobsList.size,
        ...filters,
        test_type: 'job',
      },
      op: 'jobs',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'guiTest/fetchGuiJobs',
      payload: {
        page,
        size,
        ...filters,
        test_type: 'job',
      },
      op: 'jobs',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'guiTest/editGuiTest',
      payload: {
        ...data,
        test_type: 'job',
      },
      op: 'jobs',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      guiTest: { jobsList, editResult },
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
            {getFieldDecorator('jobsList', {
              initialValue: jobsList.data,
            })(
              <JobsForm
                loading={loading || searchLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                editRows={this.editRows}
                jobsList={jobsList}
                project={project}
                currentUser={currentUser}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Jobs;
