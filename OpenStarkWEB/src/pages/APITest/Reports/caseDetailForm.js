import React, { PureComponent, Fragment } from 'react';
import { Table, Button, Input, message, Divider, Row, Col, Icon } from 'antd';
import { goBack } from 'umi/router';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;

export default class CaseDetailForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      filters: {
        keyWord: '',
      },
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('detailList' in nextProps && nextProps.detailList) {
      this.setState({
        data: nextProps.detailList.data,
      });
    }
  }

  onSearchChange = filter => {
    const { filters } = this.state;
    const keyWords = filters;
    const { onSearch } = this.props;
    if (typeof filter === 'string') {
      keyWords.keyWord = filter;
    }
    onSearch(keyWords);
    this.setState({
      filters: keyWords,
    });
  };

  getRowByKey(key, newData) {
    const { data } = this.state;
    return (newData || data).filter(item => item.key === key)[0];
  }

  toggleEditable = (e, key) => {
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      // 进入编辑状态时保存原始数据
      if (!target.editable) {
        this.cacheOriginData[key] = { ...target };
      }
      target.editable = !target.editable;
      this.setState({ data: newData });
    }
  };

  handleTableChange = (pagination, filter) => {
    const { filters } = this.state;
    const search = filters;
    if (Object.keys(filter).includes('result')) {
      search.result = filter.result.join(',');
    }
    search.page = pagination.current;
    search.size = pagination.pageSize;
    this.onSearchChange(search);
  };

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      target[fieldName] = e.target ? e.target.value : e;
      this.setState({ data: newData });
    }
  }

  saveRow(e, key) {
    const { editRows } = this.props;
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.cid || !target.description) {
      message.error('请填写正确的备注信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { filters } = this.state;
    editRows(target, 'editDetail', () => {
      this.onSearchChange(filters);
    });
  }

  cancel(e, key) {
    this.clickedCancel = true;
    e.preventDefault();
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (this.cacheOriginData[key]) {
      Object.assign(target, this.cacheOriginData[key]);
      target.editable = false;
      delete this.cacheOriginData[key];
    }
    this.setState({ data: newData });
    this.clickedCancel = false;
  }

  render() {
    const {
      loading,
      detailList: { total, page },
      currentUser,
    } = this.props;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '4%',
        render: text => text,
      },
      {
        title: '用例编号',
        dataIndex: 'cid',
        key: 'cid',
        width: '8%',
        render: text => text,
      },
      {
        title: '接口标题',
        dataIndex: 'title',
        key: 'title',
        width: '15%',
        render: text => text,
      },
      {
        title: '接口',
        dataIndex: 'url',
        key: 'url',
        width: '20%',
        render: text => text,
      },
      {
        title: '请求方法',
        dataIndex: 'method',
        key: 'method',
        width: '6%',
        render: text => text,
      },
      {
        title: '响应状态',
        dataIndex: 'status',
        key: 'status',
        width: '6%',
        render: text => text,
      },
      {
        title: '开始时间',
        dataIndex: 'startTime',
        key: 'startTime',
        width: '10%',
        render: text => text,
      },
      {
        title: '结束时间',
        dataIndex: 'endTime',
        key: 'endTime',
        width: '10%',
        render: text => text,
      },
      {
        title: '响应时间(毫秒)',
        dataIndex: 'runTime',
        key: 'runTime',
        width: '10%',
        render: text => text,
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (!!record.editable && loading) {
            return null;
          }
          if (record.editable) {
            return (
              <span>
                <a onClick={e => this.saveRow(e, record.key)}>保存</a>
                <Divider type="vertical" />
                <a onClick={e => this.cancel(e, record.key)}>取消</a>
              </span>
            );
          }
          if (currentUser.authority === 'admin' || currentUser.userId === record.userId) {
            return (
              <span>
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              </span>
            );
          }
          return <span>无权限</span>;
        },
      },
    ];
    const { data } = this.state;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Button type="primary" onClick={goBack}>
              <Icon type="rollback" />
              返回
            </Button>
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按用例编号/标题/描述搜索"
              onSearch={this.onSearchChange}
              enterButton
            />
          </Col>
        </Row>
        <Table
          loading={loading}
          columns={columns}
          dataSource={data}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            hideOnSinglePage: true,
            current: page,
            total,
            showTotal: () => '共 '.concat(total).concat(' 条'),
          }}
          onChange={this.handleTableChange}
          rowClassName={record => (record.editable ? styles.editable : '')}
          expandedRowRender={record => {
            if (record.editable) {
              return (
                <Fragment>
                  <h3>请求头:</h3>
                  <TextArea
                    value={record.request_headers}
                    style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                    placeholder="请求头"
                    disabled
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                  <Divider />
                  <h3>请求体:</h3>
                  <TextArea
                    value={record.request_body}
                    style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                    placeholder="请求体"
                    disabled
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                  <Divider />
                  <h3>响应头:</h3>
                  <TextArea
                    value={record.response_headers}
                    style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                    placeholder="响应头"
                    disabled
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                  <Divider />
                  <h3>响应体:</h3>
                  <TextArea
                    value={record.response_body}
                    style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                    placeholder="响应体"
                    disabled
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                  <Divider />
                  <h3>备注:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="备注"
                    autosize={{ minRows: 5, maxRows: 25 }}
                  />
                </Fragment>
              );
            }
            return (
              <Fragment>
                <h3>请求头:</h3>
                <TextArea
                  value={record.request_headers}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="请求头"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
                <Divider />
                <h3>请求体:</h3>
                <TextArea
                  value={record.request_body}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="请求体"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
                <Divider />
                <h3>响应头:</h3>
                <TextArea
                  value={record.response_headers}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="响应头"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
                <Divider />
                <h3>响应体:</h3>
                <TextArea
                  value={record.response_body}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="响应体"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
                <Divider />
                <h3>备注:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="备注"
                  disabled
                  autosize={{ minRows: 5, maxRows: 25 }}
                />
              </Fragment>
            );
          }}
        />
      </Fragment>
    );
  }
}
