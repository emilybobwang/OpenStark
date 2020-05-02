import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import DetailForm from './detailForm';

@connect(({ user, guiTest, loading }) => ({
  guiTest,
  currentUser: user.currentUser,
  loading: loading.effects['guiTest/editGuiTest'],
  searchLoading: loading.effects['guiTest/fetchGuiDetail'],
}))
@Form.create()
class Detail extends PureComponent {
  componentDidMount() {
    const { dispatch, match } = this.props;
    const { params } = match;
    dispatch({
      type: 'guiTest/fetchGuiDetail',
      op: 'detail',
      action: 'list',
      payload: {
        jid: params.jid,
        date: params.date,
      },
    });
  }

  onSearch = filters => {
    const {
      guiTest: { detailList },
      dispatch,
      match,
    } = this.props;
    const { params } = match;
    dispatch({
      type: 'guiTest/fetchGuiDetail',
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
      type: 'guiTest/editGuiTest',
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
      guiTest: { detailList, editResult },
      loading,
      searchLoading,
      currentUser,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('detail', {
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
