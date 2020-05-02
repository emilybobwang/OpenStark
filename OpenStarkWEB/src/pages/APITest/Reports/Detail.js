import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import DetailForm from './detailForm';

@connect(({ user, apiTest, loading }) => ({
  apiTest,
  currentUser: user.currentUser,
  loading: loading.effects['apiTest/editApiTest'],
  searchLoading: loading.effects['apiTest/fetchApiDetail'],
}))
@Form.create()
class Detail extends PureComponent {
  componentDidMount() {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/fetchApiDetail',
      op: 'detail',
      action: 'list',
      payload: {
        jid: params.jid,
        date: params.date,
      },
    });
  }

  onSearch = (filters) => {
    const {
      apiTest: { detailList },
      dispatch,
      match,
    } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/fetchApiDetail',
      payload: {
        size: detailList.size,
        ...filters,
        jid: params.jid,
        date: params.date,
      },
      op: 'detail',
      action: 'list',
    });
  };

  editRows = (data, action, callback) => {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'apiTest/editApiTest',
      payload: {
        ...data,
        jid: params.jid,
        date: params.date,
      },
      op: 'detail',
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
    const { getFieldDecorator } = form;
    const { params } = match;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator(params.jid, {
              initialValue: detailList.data,
            })(
              <DetailForm
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

export default Detail;
