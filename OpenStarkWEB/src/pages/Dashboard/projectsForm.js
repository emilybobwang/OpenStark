import React, { PureComponent, Fragment } from 'react';
import {
  Table,
  Button,
  Input,
  message,
  Popconfirm,
  Divider,
  Select,
  Row,
  Col,
  Pagination,
  Modal,
  Icon,
} from 'antd';
import styles from '../Tools/style.less';

const { TextArea, Search } = Input;
const { Option } = Select;

export default class ProjectsForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      filters: {
        name: '',
      },
      removeKeys: [],
      visible: false,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('newData' in nextProps) {
      this.setState({
        data: nextProps.newData,
      });
    }
  }

  onPageChange = (page, pageSize) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(page, pageSize, filters);
  };

  onShowSizeChange = (current, size) => {
    const { onShowSizeChange } = this.props;
    const { filters } = this.state;
    onShowSizeChange(current, size, filters);
  };

  onSearch = filter => {
    const { filters } = this.state;
    const { onSearch } = this.props;
    if (typeof filter === 'string') {
      filters.name = filter;
    }
    onSearch(filters);
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
    const { currentUser } = this.props;
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    const department = currentUser.department.split('/');
    newData.push({
      no: `TEMP_ID_${this.index}`,
      key: `NEW_TEMP_ID_${this.index}`,
      name: '',
      tid: currentUser.department_id.length === 3 ? currentUser.department_id[2] : '',
      pid: '',
      team:
        department.length === 3
          ? department[2]
              .trim()
              .concat(' (')
              .concat(department[1].trim())
              .concat(')')
          : '',
      description: '',
      params: '',
      status: 1,
      userId: currentUser.userId,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  handleOk = () => {
    this.setState({
      visible: false,
    });
  };

  handleCancel = () => {
    this.setState({
      visible: false,
    });
  };

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleTableChange = (_, filter) => {
    const { filters } = this.state;
    if (Object.keys(filter).includes('tid')) {
      filters.tid = filter.tid.join(',');
    }
    this.onSearch(filters);
  };

  onSelectChange = (selectedRowKeys, selectedRows) => {
    const { currentUser } = this.props;
    const { removeKeys } = this.state;
    const selected = selectedRows
      .filter(element => currentUser.authority === 'admin' || element.userId === currentUser.userId)
      .map(item => item.pid);
    this.setState({
      removeKeys: selectedRowKeys.filter(
        item => removeKeys.indexOf(item) >= 0 || selected.indexOf(item) >= 0
      ),
    });
  };

  removeRows = () => {
    const { removeRow } = this.props;
    const { data, removeKeys, filters } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      removeRow({ pid: rowKeys }, ()=>{
        this.onSearch(filters);
      });
    }
    this.setState({
      removeKeys: [],
    });
  };

  saveRow(e, key) {
    e.persist();

    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.tid || !target.name || !target.status) {
      message.error('请填写完整的项目信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { saveRow } = this.props;
    const { filters } = this.state;
    saveRow(target, ()=>{
      this.onSearch(filters);
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

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  handleFieldChange(e, fieldName, key) {
    const { data } = this.state;
    const { teamsData } = this.props;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      const value = e.target ? e.target.value : e;
      target[fieldName] = value;
      if (fieldName === 'tid') {
        target.team = teamsData.filter(item => item.tid === value)[0].name;
      }
      this.setState({ data: newData });
    }
  }

  remove(record) {
    const { data, filters } = this.state;
    const { removeRow } = this.props;
    const newData = data.filter(item => item.key !== record.key);
    this.setState({ data: newData });
    if (typeof record.pid === 'number') {
      removeRow(record, ()=>{
        this.onSearch(filters);
      });
    }
  }

  render() {
    const { teamsData, page, total, loading } = this.props;
    const { data, visible, removeKeys } = this.state;
    const hasSelected = removeKeys.length > 0;
    const option = teamsData.map(item => (
      <Option key={item.tid} value={item.tid}>
        {item.name}
      </Option>
    ));
    const { currentUser } = this.props;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'key',
        width: '8%',
        render: text => text,
      },
      {
        title: '项目编号',
        dataIndex: 'pid',
        key: 'pid',
        width: '8%',
        render: text => text,
      },
      {
        title: '所属组',
        dataIndex: 'team',
        key: 'tid',
        width: '15%',
        filterMultiple: false,
        filters: teamsData.map(item => ({ text: item.name, value: item.tid })),
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text}
                value={text}
                onChange={e => this.handleFieldChange(e, 'tid', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="所属组"
              >
                {option}
              </Select>
            );
          }
          return text;
        },
      },
      {
        title: '项目名称',
        dataIndex: 'name',
        key: 'name',
        width: '15%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                autoFocus
                value={text}
                onChange={e => this.handleFieldChange(e, 'name', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="项目名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '项目描述',
        dataIndex: 'description',
        key: 'description',
        width: '30%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <TextArea
                value={text}
                onChange={e => this.handleFieldChange(e, 'description', record.key)}
                placeholder="项目描述"
              />
            );
          }
          return (
            <TextArea
              value={text}
              style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
              placeholder="项目描述"
              disabled
            />
          );
        },
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text.toString()}
                value={text.toString()}
                onChange={e => this.handleFieldChange(e, 'status', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="状态"
              >
                <Option value="1">启用</Option>
                <Option value="0">禁用</Option>
              </Select>
            );
          }
          return text.toString() === '1' ? '启用' : '禁用';
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
                <a onClick={this.showModal}>项目参数</a>
                <Divider type="vertical" />
                <Popconfirm
                  title="统计数据将被清空, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
              </span>
            );
          }
          return (
            <span>
              <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              <Divider type="vertical" />
              <a onClick={this.showModal}>项目参数</a>
            </span>
          );
        },
      },
    ];

    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Popconfirm
              title="将会删除所选项目相关的信息, 是否要删除？"
              onConfirm={() => this.removeRows()}
            >
              <Button type="primary" disabled={!hasSelected}>
                <Icon type="delete" />
                批量删除
              </Button>
            </Popconfirm>
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按项目名称搜索"
              onSearch={this.onSearch}
              enterButton
            />
          </Col>
        </Row>
        <Table
          rowSelection={{
            selections: true,
            onChange: this.onSelectChange,
          }}
          loading={loading}
          columns={columns}
          dataSource={data}
          pagination={false}
          onChange={this.handleTableChange}
          rowClassName={record => (record.editable ? styles.editable : '')}
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增项目
        </Button>
        <Row>
          <Col style={{ textAlign: 'right' }}>
            <Pagination
              style={{ marginTop: 16 }}
              showSizeChanger
              showQuickJumper
              hideOnSinglePage
              current={page}
              onChange={this.onPageChange}
              onShowSizeChange={this.onShowSizeChange}
              total={total}
              showTotal={() => '共 '.concat(total.toString()).concat(' 条')}
            />
          </Col>
        </Row>
        <Modal
          title="项目参数"
          visible={visible}
          onOk={this.handleOk}
          confirmLoading={loading}
          onCancel={this.handleCancel}
        >
          <p>这里是表单</p>
        </Modal>
      </Fragment>
    );
  }
}
