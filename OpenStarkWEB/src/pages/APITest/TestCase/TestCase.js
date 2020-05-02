import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import TestCaseForm from './testCaseForm';

@connect(({ user, apiTest, project, loading }) => ({
  apiTest,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['apiTest/editApiTest'],
  searchLoading: loading.effects['apiTest/fetchApiTest'],
}))
@Form.create()
class TestCase extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'apiTest/fetchApiTest',
      op: 'testCase',
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
      apiTest: { testCases },
      dispatch,
    } = this.props;
    dispatch({
      type: 'apiTest/fetchApiTest',
      payload: {
        size: testCases.size,
        ...filters,
      },
      op: 'testCase',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'apiTest/fetchApiTest',
      payload: {
        page,
        size,
        ...filters,
      },
      op: 'testCase',
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
      op: 'testCase',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      apiTest: { testCases, editResult },
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
            {getFieldDecorator('testCase', {
              initialValue: testCases.data,
            })(
              <TestCaseForm
                loading={loading || searchLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                editRows={this.editRows}
                testCases={testCases}
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

export default TestCase;
