import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import TestCaseDetailForm from './testCaseDetailForm';

@connect(({ user, apiTest, loading }) => ({
  apiTest,
  currentUser: user.currentUser,
  loading: loading.effects['apiTest/editApiTest'],
  searchLoading: loading.effects['apiTest/fetchApiDetail'],
}))
@Form.create()
class TestCaseDetail extends PureComponent {
  componentDidMount() {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/fetchApiDetail',
      op: 'testCase',
      action: 'detail',
      payload: {
        cid: params.cid,
        pid: params.pid,
      },
    });
  }

  onSearch = filters => {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/fetchApiDetail',
      payload: {
        ...filters,
        cid: params.cid,
        pid: params.pid,
      },
      op: 'testCase',
      action: 'detail',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/editApiTest',
      payload: {
        ...data,
        cid: params.cid,
        pid: params.pid,
      },
      op: 'testCase',
      action,
      callback,
    });
  };

  render() {
    const {
      form,
      apiTest: { detailList, editResult },
      loading,
      searchLoading,
      currentUser,
      match,
    } = this.props;
    const { params } = match;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator(params.cid, {
              initialValue: detailList.data,
            })(
              <TestCaseDetailForm
                loading={loading || searchLoading}
                editStatus={editResult}
                onSearch={this.onSearch}
                editRows={this.editRows}
                detailList={detailList}
                currentUser={currentUser}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default TestCaseDetail;
