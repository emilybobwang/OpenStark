import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import EnvDetailForm from './envDetailForm';

@connect(({ user, environment, loading }) => ({
  environment,
  currentUser: user.currentUser,
  loading: loading.effects['environment/editEnv'],
  searchLoading: loading.effects['environment/fetchEnvDetail'],
}))
@Form.create()
class EnvDetail extends PureComponent {
  componentDidMount() {
    const { match, dispatch } = this.props;
    const { params } = match;
    dispatch({
      type: 'environment/fetchEnvDetail',
      op: 'detail',
      action: 'list',
      payload: {
        eid: params.eid,
      },
    });
  }

  onSearch = filters => {
    const {
      environment: { envList },
      match,
      dispatch,
    } = this.props;
    const { params } = match;
    dispatch({
      type: 'environment/fetchEnvDetail',
      payload: {
        size: envList.size,
        ...filters,
        eid: params.eid,
      },
      op: 'detail',
      action: 'list',
    });
  };

  onPageChange = (page, size, filters) => {
    const { match, dispatch } = this.props;
    const { params } = match;
    dispatch({
      type: 'environment/fetchEnvDetail',
      payload: {
        page,
        size,
        ...filters,
        eid: params.eid,
      },
      op: 'detail',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { match, dispatch } = this.props;
    const { params } = match;
    dispatch({
      type: 'environment/editEnv',
      payload: {
        ...data,
        eid: params.eid,
      },
      op: 'detail',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      environment: { detailList, editResult },
      loading,
      currentUser,
      searchLoading,
      match,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('detail', {
              initialValue: detailList.data,
            })(
              <EnvDetailForm
                loading={loading || searchLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                editRows={this.editRows}
                detailList={detailList}
                currentUser={currentUser}
                match={match}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default EnvDetail;
