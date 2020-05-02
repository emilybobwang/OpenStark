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
  Icon,
  Modal,
  Spin,
} from 'antd';
import Link from 'umi/link';
import jsonp from 'fetch-jsonp';
import querystring from 'querystring';
import styles from '../../Tools/style.less';

const { TextArea, Search } = Input;
const { Option } = Select;

export default class EnvironmentForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      removeKeys: [],
      filters: {
        keyWord: '',
      },
      visible: false,
      modalContent: undefined,
      users: [],
      userLoading: false,
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('envList' in nextProps && nextProps.envList) {
      this.setState({
        data: nextProps.envList.data,
      });
    }
    if ('editStatus' in nextProps && nextProps.editStatus) {
      if (
        nextProps.editStatus.status === 'SUCCESS' &&
        typeof nextProps.editStatus.data === 'string'
      ) {
        this.setState({
          modalContent: (
            <TextArea
              value={nextProps.editStatus.data}
              style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
              placeholder="环境HOST信息"
              disabled
              autosize
            />
          ),
        });
      }
    }
  }

  onSearchUser = data => {
    const str = querystring.encode({
      type: 'members',
      name: data,
      size: 0,
    });
    this.setState({ userLoading: true });
    jsonp(`${window.location.origin}/api/py/group/getTeams?${str}`)
      .then(response => response.json())
      .then(resp => {
        const users = [];
        resp.forEach(item => {
          users.push({
            uid: item.uid,
            username: item.username,
            name: item.name,
            dep: item.department.value && item.department.value[item.department.value.length - 1],
          });
        });
        this.setState({ users });
      })
      .finally(() => {
        this.setState({ userLoading: false });
      });
  };

  onPageChange = (page, pageSize) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(page, pageSize, filters);
  };

  onShowSizeChange = (current, size) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(current, size, filters);
  };

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

  onSelectChange = selectedRowKeys => {
    const { currentUser } = this.props;
    if (currentUser.authority === 'admin') {
      this.setState({
        removeKeys: selectedRowKeys,
      });
    }
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

  removeRows = () => {
    const { editRows } = this.props;
    const { data, removeKeys, filters } = this.state;
    const newData = data.filter(item => removeKeys.indexOf(item.key) === -1);
    const rowKeys = removeKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      editRows({ key: rowKeys }, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: [],
    });
  };

  newMember = () => {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      no: `NEW_TEMP_ID_${this.index}`,
      key: `NEW_TEMP_KEY_${this.index}`,
      eid: '',
      title: '',
      type: 'function',
      description: '',
      principal: '',
      uid: '',
      username: '',
      dep: '',
      status: 1,
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  showModal = eid => {
    this.setState({
      visible: true,
      modalContent: (
        <p style={{ textAlign: 'center' }}>
          <Icon type="loading" />
        </p>
      ),
    });
    const { editRows } = this.props;
    editRows({ eid }, 'host');
  };

  handleTableChange = (_, filter) => {
    const { filters } = this.state;
    const search = filters;
    if (Object.keys(filter).includes('type')) {
      search.type = filter.type.join(',');
    }
    if (Object.keys(filter).includes('status')) {
      search.status = filter.status.join(',');
    }
    this.onSearchChange(search);
  };

  handleFieldChange(e, fieldName, key) {
    const { data, users } = this.state;
    const newData = data.map(item => ({ ...item }));
    const target = this.getRowByKey(key, newData);
    if (target) {
      const tValue = e && e.target ? e.target.value : e;
      if (fieldName === 'uid') {
        const user = users.filter(item => item.uid === tValue);
        target.uid = tValue;
        target.principal = user[0].name;
        target.username = user[0].username;
        target.dep = user[0].dep;
      } else {
        target[fieldName] = tValue;
      }
      this.setState({
        data: newData,
      });
    }
  }

  handleKeyPress(e, key) {
    if (e.key === 'Enter') {
      this.saveRow(e, key);
    }
  }

  remove(record) {
    const { data, filters, removeKeys } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      editRows(record, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      removeKeys: removeKeys.filter(item => item !== record.key),
    });
  }

  saveRow(e, key) {
    const { editRows } = this.props;
    e.persist();
    if (this.clickedCancel) {
      this.clickedCancel = false;
      return;
    }
    const target = this.getRowByKey(key) || {};
    if (!target.type || !target.title) {
      message.error('请填写完整的环境信息。');
      e.target.focus();
      return;
    }
    this.toggleEditable(e, key);
    const { filters } = this.state;
    editRows(target, 'edit', ()=>{
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
      envList: { total, page },
      currentUser,
    } = this.props;
    const { userLoading, users } = this.state;
    const columns = [
      {
        title: '#',
        dataIndex: 'no',
        key: 'no',
        width: '4%',
        render: text => text,
      },
      {
        title: '环境编号',
        dataIndex: 'eid',
        key: 'eid',
        width: '12%',
        render: text => text,
      },
      {
        title: '环境名称',
        dataIndex: 'title',
        key: 'title',
        width: '15%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'title', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="环境名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '环境类型',
        dataIndex: 'type',
        key: 'type',
        width: '10%',
        filters: [
          { text: '功能测试', value: 'function' },
          { text: '集成测试', value: 'Integration' },
          { text: '性能测试', value: 'performance' },
          { text: '自动化测试', value: 'automation' },
        ],
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text}
                value={text}
                onChange={e => this.handleFieldChange(e, 'type', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="环境类型"
              >
                <Option value="function">功能测试</Option>
                <Option value="Integration">集成测试</Option>
                <Option value="performance">性能测试</Option>
                <Option value="automation">自动化测试</Option>
              </Select>
            );
          }
          let type = '功能测试';
          switch (text) {
            case 'function':
              type = '功能测试';
              break;
            case 'Integration':
              type = '集成测试';
              break;
            case 'performance':
              type = '性能测试';
              break;
            case 'automation':
              type = '自动化测试';
              break;
            default:
              break;
          }
          return type;
        },
      },
      {
        title: '环境描述',
        dataIndex: 'description',
        key: 'description',
        width: '20%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <TextArea
                value={record.description}
                onChange={e => this.handleFieldChange(e, 'description', record.key)}
                placeholder="环境描述"
                autosize
              />
            );
          }
          return (
            <TextArea
              value={record.description}
              style={{ backgroundColor: '#fff', color: 'rgba(0, 0, 0, 0.65)' }}
              placeholder="环境描述"
              disabled
              autosize
            />
          );
        },
      },
      {
        title: '负责人',
        dataIndex: 'principal',
        key: 'principal',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                showSearch
                value={text}
                style={{ width: '100%' }}
                placeholder="负责人"
                defaultActiveFirstOption={false}
                showArrow={false}
                filterOption={false}
                notFoundContent={userLoading ? <Spin size="small" /> : null}
                onSearch={e => this.onSearchUser(e)}
                onChange={e => this.handleFieldChange(e, 'uid', record.key)}
              >
                {users.map(item => (
                  <Option key={item.uid} value={item.uid} title={item.username}>
                    {item.name}
                  </Option>
                ))}
              </Select>
            );
          }
          return text
            ? text
                .concat('(')
                .concat(record.username)
                .concat(')')
            : '';
        },
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '8%',
        filters: [
          { text: '正常', value: '1' },
          { text: '不可用', value: '0' },
          { text: '服务异常', value: '2' },
        ],
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text.toString()}
                value={text.toString()}
                onChange={e => this.handleFieldChange(e, 'status', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="环境类型"
              >
                <Option value="1">正常</Option>
                <Option value="0">不可用</Option>
                <Option value="2">服务异常</Option>
              </Select>
            );
          }
          if ((text || '0').toString() === '0') {
            return '不可用';
          }
          if ((text || '0').toString() === '1') {
            return '正常';
          }
          return '服务异常';
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
          if (currentUser.authority === 'admin') {
            return (
              <span>
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
                <Divider type="vertical" />
                <Popconfirm
                  title="将会删除该环境相关的所有配置信息, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
                <Divider type="vertical" />
                <Link to={`/dashboard/environment/detail/${record.dep || 0}/${record.eid}`}>
                  服务器信息
                </Link>
                <Divider type="vertical" />
                <a
                  onClick={() => {
                    this.showModal(record.eid);
                  }}
                >
                  HOST信息
                </a>
              </span>
            );
          }
          return (
            <span>
              <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
              <Divider type="vertical" />
              <Link to={`/dashboard/environment/detail/${record.dep || 0}/${record.eid}`}>
                服务器信息
              </Link>
              <Divider type="vertical" />
              <a
                onClick={() => {
                  this.showModal(record.eid);
                }}
              >
                HOST信息
              </a>
            </span>
          );
        },
      },
    ];
    const { removeKeys, data, visible, modalContent } = this.state;
    const hasSelected = removeKeys.length > 0;

    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Popconfirm
              title="将会删除所选环境相关的所有配置信息, 是否要删除？"
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
              placeholder="按环境编号/名称/描述搜索"
              onSearch={this.onSearchChange}
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
          新增环境信息
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
          title="环境HOST信息"
          visible={visible}
          onCancel={() => {
            this.setState({
              visible: false,
            });
          }}
          footer={null}
          width={800}
        >
          {modalContent}
        </Modal>
      </Fragment>
    );
  }
}
