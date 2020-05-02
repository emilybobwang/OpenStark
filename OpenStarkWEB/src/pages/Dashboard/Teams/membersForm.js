import React, { PureComponent, Fragment } from 'react';
import {
  Table,
  Button,
  Input,
  message,
  Popconfirm,
  Divider,
  Select,
  Cascader,
  Row,
  Col,
  Pagination,
} from 'antd';
import styles from '../style.less';

const { Search } = Input;
const { Option } = Select;

export default class MembersForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
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
    onPageChange({
      page,
      size: pageSize,
      type: 'members',
    });
  };

  onShowSizeChange = (current, size) => {
    const { onShowSizeChange } = this.props;
    onShowSizeChange({
      page: current,
      size,
      type: 'members',
    });
  };

  onSearch = data => {
    const { onSearch } = this.props;
    onSearch({
      name: data,
      type: 'members',
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

  resetPasswd = record => {
    const { saveRow } = this.props;
    saveRow({
      type: 'reset',
      data: record,
    });
  };

  newMember = () => {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      key: `NEW_TEMP_ID_${this.index}`,
      uid: '',
      username: '',
      workId: '',
      name: '',
      email: '',
      position: '',
      department: {
        value: [],
        label: '',
      },
      role: 1,
      status: 2,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  remove(record) {
    const { data } = this.state;
    const { removeRow, id } = this.props;
    const newData = data.filter(item => item.key !== record.key);
    this.setState({ data: newData });
    if (typeof record.uid === 'number') {
      removeRow({ type: id, data: record });
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
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.username || !target.name || !target.email) {
      message.error('请填写完整的成员信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { saveRow, id } = this.props;
    saveRow({
      type: id,
      data: {
        ...target,
        department: Array.isArray(target.department) ? target.department : target.department.value,
      },
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
    const { departments, loading, page, total } = this.props;
    const { data } = this.state;
    const columns = [
      {
        title: '#',
        dataIndex: 'key',
        key: 'key',
        width: '4%',
        render: text => text,
      },
      {
        title: '用户名',
        dataIndex: 'username',
        key: 'uid',
        width: '10%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'username', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="用户名"
              />
            );
          }
          return text;
        },
      },
      {
        title: '姓名',
        dataIndex: 'name',
        key: 'name',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'name', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="姓名"
              />
            );
          }
          return text;
        },
      },
      {
        title: '工号',
        dataIndex: 'workerId',
        key: 'workerId',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'workerId', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="工号"
              />
            );
          }
          return text;
        },
      },
      {
        title: '邮箱',
        dataIndex: 'email',
        key: 'email',
        width: '15%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'email', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="邮箱"
              />
            );
          }
          return text;
        },
      },
      {
        title: '职位',
        dataIndex: 'position',
        key: 'position',
        width: '10%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'position', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="职位"
              />
            );
          }
          return text;
        },
      },
      {
        title: '所属团队',
        dataIndex: 'department',
        key: 'department',
        width: '18%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Cascader
                defaultValue={text.value}
                options={departments}
                onChange={e => this.handleFieldChange(e, 'department', record.key)}
                placeholder="所属团队"
                style={{ width: '100%' }}
                changeOnSelect
              />
            );
          }
          return text.label;
        },
      },
      {
        title: '角色',
        dataIndex: 'role',
        key: 'role',
        width: '6%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text.toString()}
                value={text.toString()}
                onChange={e => this.handleFieldChange(e, 'role', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="角色"
              >
                <Option value="1">普通用户</Option>
                <Option value="0">管理员</Option>
              </Select>
            );
          }
          return text.toString() === '1' ? '普通用户' : '管理员';
        },
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '6%',
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
                <Option value="2">正常</Option>
                <Option value="1">未激活</Option>
                <Option value="0">禁用</Option>
              </Select>
            );
          }
          if (text.toString() === '1') {
            return '未激活';
          }
          if (text.toString() === '0') {
            return '禁用';
          }
          return '正常';
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
          return (
            <span>
              <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              <Divider type="vertical" />
              <Popconfirm
                title="将会删除该用户所有的信息, 是否要删除此行？"
                onConfirm={() => this.remove(record)}
              >
                <a>删除</a>
              </Popconfirm>
              <Divider type="vertical" />
              <Popconfirm title="确定要重置该用户密码？" onConfirm={() => this.resetPasswd(record)}>
                <a>重置密码</a>
              </Popconfirm>
            </span>
          );
        },
      },
    ];

    return (
      <Fragment>
        <Row>
          <Col span={4} offset={20}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按用户名/姓名/工号/邮箱搜索"
              onSearch={this.onSearch}
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
        />
        <Button
          style={{ width: '100%', marginTop: 16, marginBottom: 8 }}
          type="dashed"
          onClick={this.newMember}
          icon="plus"
        >
          新增成员
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
      </Fragment>
    );
  }
}
