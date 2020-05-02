import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import EnvironmentForm from './environmentForm';

@connect(({ user, environment, loading }) => ({
  currentUser: user.currentUser,
  environment,
  loading: loading.effects['environment/editEnv'],
  searchLoading: loading.effects['environment/fetchEnv'],
}))
@Form.create()
class Environment extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      op: 'server',
      action: 'list',
    });
  }

  onSearch = filters => {
    const {
      environment: { envList },
      dispatch,
    } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      payload: {
        size: envList.size,
        ...filters,
      },
      op: 'server',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/fetchEnv',
      payload: {
        page,
        size,
        ...filters,
      },
      op: 'server',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'environment/editEnv',
      payload: {
        ...data,
      },
      op: 'server',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      environment: { envList, editResult },
      loading,
      searchLoading,
      currentUser,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('envList', {
              initialValue: envList.data,
            })(
              <EnvironmentForm
                loading={loading || searchLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                editRows={this.editRows}
                envList={envList}
                currentUser={currentUser}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Environment;
