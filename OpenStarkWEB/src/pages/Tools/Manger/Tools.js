import React, { PureComponent, Fragment } from 'react';
import { Card, Form } from 'antd';
import { connect } from 'dva';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import ToolsForm from './toolsForm';

@connect(({ user, tools, loading }) => ({
  currentUser: user.currentUser,
  tools,
  loading: loading.effects['tools/fetchTools'],
  edLoading: loading.effects['tools/editTools'],
  deLoading: loading.effects['tools/deleteTools'],
}))
@Form.create()
class Tools extends PureComponent {
  state = {
    name: '',
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/fetchTools',
    });
  }

  onSearch = data => {
    const {
      tools: { tools },
      dispatch,
    } = this.props;
    dispatch({
      type: 'tools/fetchTools',
      payload: {
        name: data,
        size: tools.size,
      },
    });
    this.setState({
      name: data,
    });
  };

  onPageChange = (page, pageSize) => {
    const { dispatch } = this.props;
    const { name } = this.state;
    dispatch({
      type: 'tools/fetchTools',
      payload: {
        page,
        size: pageSize,
        name,
      },
    });
  };

  onShowSizeChange = (current, size) => {
    const { dispatch } = this.props;
    const { name } = this.state;
    dispatch({
      type: 'tools/fetchTools',
      payload: {
        page: current,
        size,
        name,
      },
    });
  };

  saveRow = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/editTools',
      payload: data,
      callback:()=>{
        this.onSearch();
      },
    });
  };

  removeRow = data => {
    const { dispatch } = this.props;
    dispatch({
      type: 'tools/deleteTools',
      payload: data,
      callback:()=>{
        this.onSearch();
      },
    });
  };

  render() {
    const { form, tools, currentUser, loading, edLoading, deLoading } = this.props;
    const { getFieldDecorator } = form;
    return (
      <PageHeaderWrapper>
        <Fragment>
          <Card bordered={false}>
            {getFieldDecorator('tools', {
              initialValue: tools.tools.data,
            })(
              <ToolsForm
                loading={loading || edLoading || deLoading}
                saveRow={this.saveRow}
                removeRow={this.removeRow}
                editStatus={tools.editResult}
                onSearch={this.onSearch}
                onPageChange={this.onPageChange}
                onShowSizeChange={this.onShowSizeChange}
                page={tools.tools.page}
                size={tools.tools.size}
                total={tools.tools.total}
                newData={tools.tools.data}
                currentUser={currentUser}
              />
            )}
          </Card>
        </Fragment>
      </PageHeaderWrapper>
    );
  }
}

export default Tools;
