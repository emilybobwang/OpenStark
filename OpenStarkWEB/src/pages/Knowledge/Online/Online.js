import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import OnlineForm from './onlineForm';

@connect(({ user, knowledge, project, loading }) => ({
  knowledge,
  currentUser: user.currentUser,
  teams: project.teams,
  loading: loading.effects['knowledge/editBooks'],
  searchLoading: loading.effects['knowledge/getOnline'],
  confirmLoading: loading.effects['global/sendMail'],
}))
@Form.create()
class Online extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'knowledge/getOnline',
      op: 'online',
      action: 'list',
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
      knowledge: { online },
      dispatch,
    } = this.props;
    dispatch({
      type: 'knowledge/getOnline',
      payload: {
        size: online.size,
        ...filters,
      },
      op: 'online',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'knowledge/getOnline',
      payload: {
        page,
        size,
        ...filters,
      },
      op: 'online',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'knowledge/editBooks',
      payload: {
        ...data,
      },
      op: 'online',
      action,
      callback,
    });
  };

  sendMail = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'global/sendMail',
      payload: {
        ...data,
      },
      op: 'online',
    });
  };

  render() {
    const {
      form,
      knowledge: { online, editResult },
      teams,
      loading,
      searchLoading,
      currentUser,
      confirmLoading,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('online', {
              initialValue: online.data,
            })(
              <OnlineForm
                loading={loading || searchLoading || confirmLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                editRows={this.editRows}
                online={online}
                teams={teams}
                currentUser={currentUser}
                sendMail={this.sendMail}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Online;
