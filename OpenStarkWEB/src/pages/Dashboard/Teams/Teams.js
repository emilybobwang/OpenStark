import React, { PureComponent, Fragment } from 'react';
import { Card, Form, Tabs } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import GroupForm from './groupForm';
import MembersForm from './membersForm';

const { TabPane } = Tabs;

@connect(({ teams, user, loading }) => ({
  teams,
  departments: user.departments,
  loading: loading.effects['teams/fetchTeams'],
  editLoading: loading.effects['teams/editTeams'],
  deleteLoading: loading.effects['teams/deleteTeams'],
}))
@Form.create()
class Teams extends PureComponent {
  state = {
    name: '',
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'teams/fetchTeams',
    });
    dispatch({
      type: 'user/getDepartments',
    });
  }

  onSearch = data => {
    const {
      teams: { members },
      dispatch,
    } = this.props;
    dispatch({
      type: 'teams/fetchTeams',
      payload: {
        size: members.size,
        ...data,
      },
    });
    this.setState({
      name: data.name,
    });
  };

  onPageChange = data => {
    const { dispatch } = this.props;
    const { name } = this.state;
    dispatch({
      type: 'teams/fetchTeams',
      payload: {
        name,
        ...data,
      },
    });
  };

  onShowSizeChange = data => {
    const { dispatch } = this.props;
    const { name } = this.state;
    dispatch({
      type: 'teams/fetchTeams',
      payload: {
        name,
        ...data,
      },
    });
  };

  saveRow = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'teams/editTeams',
      payload: data,
      callback: ()=>{
        dispatch({
          type: 'teams/fetchTeams',
          payload: {
            type: data.type,
          },
        });
      },
    });
  };

  removeRow = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'teams/deleteTeams',
      payload: data,
      callback: ()=>{
        dispatch({
          type: 'teams/fetchTeams',
          payload: {
            type: data.type,
          },
        });
      },
    });
  };

  render() {
    const { form, teams, departments, loading, editLoading, deleteLoading } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            <Tabs size="large" tabBarStyle={{ marginBottom: 24 }}>
              <TabPane tab="团队管理" key="groups">
                {getFieldDecorator('groups', {
                  initialValue: teams.groups,
                })(
                  <GroupForm
                    saveRow={this.saveRow}
                    removeRow={this.removeRow}
                    data={teams.groups}
                    editStatus={teams.editResult}
                    loading={loading || editLoading || deleteLoading}
                  />
                )}
              </TabPane>
              <TabPane tab="成员管理" key="members">
                {getFieldDecorator('members', {
                  initialValue: teams.members.data,
                })(
                  <MembersForm
                    saveRow={this.saveRow}
                    removeRow={this.removeRow}
                    editStatus={teams.editResult}
                    departments={departments}
                    onSearch={this.onSearch}
                    onPageChange={this.onPageChange}
                    onShowSizeChange={this.onShowSizeChange}
                    page={teams.members.page}
                    size={teams.members.size}
                    total={teams.members.total}
                    newData={teams.members.data}
                    loading={loading || editLoading || deleteLoading}
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

export default Teams;
