import React, { PureComponent, Fragment } from 'react';
import { connect } from 'dva';
import { Form } from 'antd';
import NavForm from './navForm';

@connect(({ user, loading }) => ({
  user,
  loading: loading.effects['user/deleteLink'],
  submitting: loading.effects['user/addLink'],
}))
@Form.create()
class Setting extends PureComponent {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/getOwnLink',
    });
  }

  saveRow = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/addLink',
      payload: data,
      callback: ()=>{
        dispatch({
          type: 'user/getOwnLink',
        });
      },
    });
  };

  removeRow = (data) => {
    const { dispatch } = this.props;
    dispatch({
      type: 'user/deleteLink',
      payload: data,
      callback: ()=>{
        dispatch({
          type: 'user/getOwnLink',
        });
      },
    });
  };

  render() {
    const {
      form,
      user: { navOwnLinks, editResult },
      submitting,
      loading,
    } = this.props;
    const { getFieldDecorator } = form;
    return (
      <Fragment>
        {getFieldDecorator('navLink', {
          initialValue: navOwnLinks,
        })(
          <NavForm
            editStatus={editResult}
            loading={submitting || loading}
            saveRow={this.saveRow}
            removeRow={this.removeRow}
            data={navOwnLinks}
          />
        )}
      </Fragment>
    );
  }
}

export default Setting;
