import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import JobsForm from './jobsForm';

@connect(({ user, apiTest, project, loading }) => ({
  apiTest,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['apiTest/editApiTest'],
  searchLoading: loading.effects['apiTest/fetchApiJobs'],
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
      type: 'apiTest/fetchApiJobs',
      op: 'jobs',
      action: 'list',
    });
  }

  onSearch = filters => {
    const {
      apiTest: { jobsList },
      dispatch,
    } = this.props;
    dispatch({
      type: 'apiTest/fetchApiJobs',
      payload: {
        size: jobsList.size,
        ...filters,
      },
      op: 'jobs',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'apiTest/fetchApiJobs',
      payload: {
        page,
        size,
        ...filters,
      },
      op: 'jobs',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'apiTest/editApiTest',
      payload: {
        ...data,
      },
      op: 'jobs',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      apiTest: { jobsList, editResult },
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
