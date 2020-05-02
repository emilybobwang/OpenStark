import React, { PureComponent, Fragment } from 'react';
import { Table, Button, Input, message, Divider, Row, Col, Icon, Popconfirm } from 'antd';
import { goBack } from 'umi/router';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;

export default class TestCaseDetailForm extends PureComponent {
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

  newMember = () => {
    const { currentUser, id } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      no: `NEW_TEMP_ID_${this.index}`,
      key: `NEW_TEMP_KEY_${this.index}`,
      title: '',
      cid: id,
      url: '',
      method: 'POST',
      request_headers: '',
      request_body: '',
      description: '',
      userId: currentUser.userId,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  remove(record) {
    const { data, filters } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      editRows(record, 'deleteDetail', ()=>{
        this.onSearchChange(filters);
      });
    }
  }

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
    if (!target.cid || !target.title || !target.url || !target.method) {
      message.error('请填写正确的接口信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { filters } = this.state;
    editRows(target, 'editDetail', ()=>{
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
    const { loading, currentUser } = this.props;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '8%',
        render: text => text,
      },
      {
        title: '用例编号',
        dataIndex: 'cid',
        key: 'cid',
        width: '10%',
        render: text => text,
      },
      {
        title: '接口标题',
        dataIndex: 'title',
        key: 'title',
        width: '20%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'title', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="接口标题"
              />
            );
          }
          return text;
        },
      },
      {
        title: '接口',
        dataIndex: 'url',
        key: 'url',
        width: '40%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                type="url"
                value={text}
                onChange={e => this.handleFieldChange(e, 'url', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="接口"
              />
            );
          }
          return text;
        },
      },
      {
        title: '请求方法',
        dataIndex: 'method',
        key: 'method',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'method', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="请求方法"
              />
            );
          }
          return text;
        },
      },
      {
        title: '操作',
        key: 'action',
        render: (text, record) => {
          if (!!record.editable && loading) {
            return null;
          }
          if (record.editable) {
            if (record.isNew) {
              return (
                <span>
                  <a onClick={e => this.saveRow(e, record.key)}>添加</a>
                  <Divider type="vertical" />
                  <Popconfirm title="是否要删除此行？" onConfirm={() => this.remove(record)}>
                    <a>删除</a>
                  </Popconfirm>
                </span>
              );
            }
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
                <Divider type="vertical" />
                <Popconfirm title="是否要删除此行？" onConfirm={() => this.remove(record)}>
                  <a>删除</a>
                </Popconfirm>
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
          pagination={false}
          rowClassName={record => (record.editable ? styles.editable : '')}
          expandedRowRender={record => {
            if (record.editable) {
              return (
                <Fragment>
                  <h3>请求头:</h3>
                  <TextArea
                    value={record.request_headers}
                    onChange={e => this.handleFieldChange(e, 'request_headers', record.key)}
                    placeholder="请求头"
                    autosize
                  />
                  <Divider />
                  <h3>请求体:</h3>
                  <TextArea
                    value={record.request_body}
                    onChange={e => this.handleFieldChange(e, 'request_body', record.key)}
                    placeholder="请求体"
                    autosize
                  />
                  <Divider />
                  <h3>备注:</h3>
                  <TextArea
                    value={record.description}
                    onChange={e => this.handleFieldChange(e, 'description', record.key)}
                    placeholder="备注"
                    autosize
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
                  autosize
                />
                <Divider />
                <h3>请求体:</h3>
                <TextArea
                  value={record.request_body}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="请求体"
                  disabled
                  autosize
                />
                <Divider />
                <h3>备注:</h3>
                <TextArea
                  value={record.description}
                  style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
                  placeholder="备注"
                  disabled
                  autosize
                />
              </Fragment>
            );
          }}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增接口
        </Button>
      </Fragment>
    );
  }
}
