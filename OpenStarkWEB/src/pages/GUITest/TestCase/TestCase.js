import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import TestCaseForm from './testCaseForm';

@connect(({ user, guiTest, project, loading }) => ({
  guiTest,
  currentUser: user.currentUser,
  project,
  loading: loading.effects['guiTest/editGuiTest'],
  searchLoading: loading.effects['guiTest/fetchGuiTest'],
}))
@Form.create()
class TestCase extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'guiTest/fetchGuiTest',
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
      guiTest: { testCases },
      dispatch,
    } = this.props;
    dispatch({
      type: 'guiTest/fetchGuiTest',
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
      type: 'guiTest/fetchGuiTest',
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
      type: 'guiTest/editGuiTest',
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
      guiTest: { testCases, editResult },
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
