import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import ProjectsForm from './projectsForm';

@connect(({ project, user, loading }) => ({
  project,
  currentUser: user.currentUser,
  loading: loading.effects['project/fetchProjects'],
  edLoading: loading.effects['project/editProjects'],
}))
@Form.create()
class Projects extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'project/fetchTeams',
      payload: {
        type: 'teams',
      },
    });
    dispatch({
      type: 'project/fetchProjects',
    });
  }

  onSearch = filters => {
    const {
      project: { projects },
      dispatch,
    } = this.props;
    dispatch({
      type: 'project/fetchProjects',
      payload: {
        size: projects.size,
        ...filters,
      },
    });
  };

  onPageChange = (page, pageSize, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'project/fetchProjects',
      payload: {
        page,
        size: pageSize,
        ...filters,
      },
    });
  };

  onShowSizeChange = (current, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'project/fetchProjects',
      payload: {
        page: current,
        size,
        ...filters,
      },
    });
  };

  saveRow = (data, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'project/editProjects',
      payload: data,
      callback,
    });
  };

  removeRow = (data, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'project/deleteProjects',
      payload: data,
      callback,
    });
  };

  render() {
    const {
      form,
      project: { projects, editResult, teams },
      currentUser,
      loading,
      edLoading,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('projects', {
              initialValue: projects.data,
            })(
              <ProjectsForm
                saveRow={this.saveRow}
                removeRow={this.removeRow}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                onShowSizeChange={this.onShowSizeChange}
                page={projects.page}
                size={projects.size}
                total={projects.total}
                newData={projects.data}
                teamsData={teams}
                currentUser={currentUser}
                loading={loading || edLoading}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Projects;
