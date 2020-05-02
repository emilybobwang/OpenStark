import React, { PureComponent, Fragment } from 'react';
import {
  Table,
  Button,
  Input,
  message,
  Select,
  Divider,
  Row,
  Col,
  Icon,
  Pagination,
  Popconfirm,
  Modal,
  DatePicker,
} from 'antd';
import { goBack } from 'umi/router';
import styles from '../../Tools/style.less';
import { getTimeDistance } from '@/utils/utils';

const { TextArea, Search } = Input;
const { Option } = Select;
const { RangePicker } = DatePicker;

export default class EnvDetailForm extends PureComponent {
  index = 0;

  cacheOriginData = {};

  constructor(props) {
    super(props);

    this.state = {
      data: props.value,
      selectedRowKeys: [],
      filters: {
        keyWord: '',
      },
      visible: false,
      rangePickerValue: getTimeDistance('today'),
    };
  }

  componentWillReceiveProps(nextProps) {
    if ('detailList' in nextProps && nextProps.detailList) {
      this.setState({
        data: nextProps.detailList.data,
      });
      if (
        'editStatus' in nextProps &&
        nextProps.editStatus &&
        nextProps.editStatus.status === 'SUCCESS' &&
        typeof nextProps.editStatus.data === 'object' &&
        nextProps.editStatus.data.length
      ) {
        this.setState({
          data: nextProps.value.map(item => ({
            ...item,
            status:
              nextProps.editStatus.data.filter(ele => ele.key === item.key).length > 0
                ? nextProps.editStatus.data.filter(ele => ele.key === item.key)[0].status
                : item.status,
            network:
              nextProps.editStatus.data.filter(ele => ele.key === item.key).length > 0
                ? nextProps.editStatus.data.filter(ele => ele.key === item.key)[0].network
                : item.network,
            mac:
              nextProps.editStatus.data.filter(ele => ele.key === item.key).length > 0 && !item.mac
                ? nextProps.editStatus.data.filter(ele => ele.key === item.key)[0].mac
                : item.mac,
          })),
        });
      }
    }
  }

  onPageChange = (page, pageSize) => {
    const { onPageChange } = this.props;
    const { filters } = this.state;
    onPageChange(page, pageSize, filters);
  };

  onShowSizeChange = (current, size) => {
    const { filters } = this.state;
    this.onPageChange(current, size, filters);
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
    this.setState({
      selectedRowKeys,
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

  removeRows = () => {
    const { editRows } = this.props;
    const { data, selectedRowKeys, filters } = this.state;
    const newData = data.filter(item => selectedRowKeys.indexOf(item.key) === -1);
    const rowKeys = selectedRowKeys.filter(item => typeof item === 'number');
    this.setState({ data: newData });
    if (rowKeys.length > 0) {
      editRows({ key: rowKeys }, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      selectedRowKeys: [],
    });
  };

  handleRangePickerChange = rangePickerValue => {
    this.setState({
      rangePickerValue,
    });
  };

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleOk = () => {
    const { editRows } = this.props;
    const { selectedRowKeys, rangePickerValue } = this.state;
    editRows(
      {
        key: selectedRowKeys,
        startTime: rangePickerValue[0].format('YYYY-MM-DD HH:mm:ss'),
        endTime: rangePickerValue[1].format('YYYY-MM-DD HH:mm:ss'),
      },
      'network'
    );
    this.setState({
      visible: false,
    });
  };

  handleCancel = () => {
    this.setState({
      visible: false,
    });
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
    if (Object.keys(filter).includes('network')) {
      search.network = filter.network.join(',');
    }
    this.onSearchChange(search);
  };

  newMember = () => {
    const { data } = this.state;
    const newData = data.map(item => ({ ...item }));
    newData.push({
      no: `NEW_TEMP_ID_${this.index}`,
      key: `NEW_TEMP_KEY_${this.index}`,
      title: '',
      type: 'OS',
      host: '',
      ip: '',
      mac: '',
      port: '',
      user: '',
      password: '',
      status: 1,
      network: 'no',
      description: '',
      editable: true,
      isNew: true,
    });
    this.index += 1;
    this.setState({ data: newData });
  };

  refreshStatus(target) {
    const { editRows } = this.props;
    const { selectedRowKeys } = this.state;
    let rowKeys = [];
    if (Object.keys(target).includes('key')) {
      rowKeys = target.key;
    } else {
      rowKeys = selectedRowKeys.filter(item => typeof item === 'number');
    }
    editRows({ key: rowKeys }, 'status');
  }

  remove(record) {
    const { data, filters, selectedRowKeys } = this.state;
    const newData = data.filter(item => item.key !== record.key);
    const { editRows } = this.props;
    this.setState({ data: newData });
    if (typeof record.key === 'number') {
      editRows(record, 'delete', ()=>{
        this.onSearchChange(filters);
      });
    }
    this.setState({
      selectedRowKeys: selectedRowKeys.filter(item => item !== record.key),
    });
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
    if (!target.title || !target.type || !target.ip || !target.port) {
      message.error('请填写正确的服务器信息。');
      e.target.focus();
      return;
    }
    if (!target.title.match(/^[a-zA-Z]+_/)) {
      message.error('名称格式为: 类型_名称, 如: Linux_应用服务器。');
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
      detailList: { total, page },
      currentUser,
      match: { params },
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
        title: '名称',
        dataIndex: 'title',
        key: 'title',
        width: '10%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                autoFocus
                onChange={e => this.handleFieldChange(e, 'title', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                title="格式为: 类型_名称, 如: mysql_数据库空库"
                placeholder="类型_名称"
              />
            );
          }
          return text;
        },
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: '8%',
        filters: [
          { text: '操作系统', value: 'OS' },
          { text: '应用服务', value: 'APPLICATION' },
          { text: '其他', value: 'OTHER' },
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
                placeholder="类型"
              >
                <Option value="OS">操作系统</Option>
                <Option value="APPLICATION">应用服务</Option>
                <Option value="OTHER">其他</Option>
              </Select>
            );
          }
          if (text === 'OS') {
            return '操作系统';
          }
          if (text === 'APPLICATION') {
            return '应用服务';
          }
          return '其他';
        },
      },
      {
        title: 'HOST',
        dataIndex: 'host',
        key: 'host',
        width: '12%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'host', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="HOST"
              />
            );
          }
          return text;
        },
      },
      {
        title: 'IP',
        dataIndex: 'ip',
        key: 'ip',
        width: '10%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'ip', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="IP"
              />
            );
          }
          return text;
        },
      },
      {
        title: '端口',
        dataIndex: 'port',
        key: 'port',
        width: '7%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'port', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="端口"
                type="number"
                min={1}
                max={65535}
              />
            );
          }
          return text;
        },
      },
      {
        title: '账号',
        dataIndex: 'user',
        key: 'user',
        width: '6%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'user', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="账号"
              />
            );
          }
          return text;
        },
      },
      {
        title: '密码',
        dataIndex: 'password',
        key: 'password',
        width: '8%',
        render: (text, record) => {
          if (record.editable) {
            return (
              <Input
                value={text}
                onChange={e => this.handleFieldChange(e, 'password', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                placeholder="密码"
              />
            );
          }
          if (
            currentUser.authority === 'admin' ||
            parseInt(params.dep, 0) ===
              (currentUser.department_id &&
                currentUser.department_id[currentUser.department_id.length - 1])
          ) {
            return text;
          }
          return '******';
        },
      },
      {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        width: '8%',
        filters: [{ text: '正常', value: '1' }, { text: '不可用', value: '0' }],
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text.toString()}
                value={text.toString()}
                onChange={e => this.handleFieldChange(e, 'status', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="状态"
              >
                <Option value="1">正常</Option>
                <Option value="0">不可用</Option>
              </Select>
            );
          }
          return text && text.toString() === '1' ? '正常' : '不可用';
        },
      },
      {
        title: '外网',
        dataIndex: 'network',
        key: 'network',
        width: '6%',
        filters: [{ text: '已开通', value: 'yes' }, { text: '未开通', value: 'no' }],
        render: (text, record) => {
          if (record.editable) {
            return (
              <Select
                defaultValue={text}
                value={text}
                onChange={e => this.handleFieldChange(e, 'network', record.key)}
                onKeyPress={e => this.handleKeyPress(e, record.key)}
                style={{ width: '100%' }}
                placeholder="外网"
              >
                <Option value="yes">已开通</Option>
                <Option value="no">未开通</Option>
              </Select>
            );
          }
          return text === 'yes' ? '已开通' : '未开通';
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
          if (
            currentUser.authority === 'admin' ||
            parseInt(params.dep, 0) ===
              (currentUser.department_id &&
                currentUser.department_id[currentUser.department_id.length - 1])
          ) {
            return (
              <span>
                <a onClick={e => this.toggleEditable(e, record.key)}>编辑</a>
                <Divider type="vertical" />
                <Popconfirm
                  title="将会删除该服务器相关的所有配置信息, 是否要删除此行？"
                  onConfirm={() => this.remove(record)}
                >
                  <a>删除</a>
                </Popconfirm>
                <Divider type="vertical" />
                <Popconfirm
                  title="确定要刷新该服务器状态？"
                  onConfirm={() => this.refreshStatus(record)}
                >
                  <a>刷新状态</a>
                </Popconfirm>
              </span>
            );
          }
          return (
            <span>
              <Popconfirm
                title="确定要刷新该服务器状态？"
                onConfirm={() => this.refreshStatus(record)}
              >
                <a>刷新状态</a>
              </Popconfirm>
            </span>
          );
        },
      },
    ];
    const { selectedRowKeys, rangePickerValue, data, visible } = this.state;
    const hasSelected = selectedRowKeys.length > 0;
    return (
      <Fragment>
        <Row>
          <Col span={20}>
            <Button type="primary" onClick={goBack}>
              <Icon type="rollback" />
              返回
            </Button>
            <Divider type="vertical" />
            <Popconfirm
              title="将会删除所选服务器相关的所有配置信息, 是否要删除？"
              onConfirm={() => this.removeRows()}
            >
              <Button type="primary" disabled={!hasSelected || currentUser.authority !== 'admin'}>
                <Icon type="delete" />
                批量删除
              </Button>
            </Popconfirm>
            <Divider type="vertical" />
            <Popconfirm title="确定要批量刷新服务器状态？" onConfirm={() => this.refreshStatus({})}>
              <Button type="primary" disabled={!hasSelected}>
                <Icon type="sync" />
                批量刷新状态
              </Button>
            </Popconfirm>
            <Divider type="vertical" />
            <Button type="primary" disabled={!hasSelected} onClick={this.showModal}>
              <Icon type="wifi" />
              开通外网
            </Button>
          </Col>
          <Col span={4}>
            <Search
              style={{ marginBottom: 20 }}
              placeholder="按名称/备注/IP等信息搜索"
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
          expandedRowRender={record => {
            if (record.editable) {
              return (
                <Fragment>
                  <h3>MAC地址:</h3>
                  <Input
                    value={record.mac}
                    onChange={e => this.handleFieldChange(e, 'mac', record.key)}
                    onKeyPress={e => this.handleKeyPress(e, record.key)}
                    placeholder="MAC地址"
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
                <h3>MAC地址:</h3>
                {record.mac}
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
          新增服务器信息
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
          title="开通外网"
          visible={visible}
          onOk={this.handleOk}
          confirmLoading={loading}
          onCancel={this.handleCancel}
        >
          <Row>
            <Col style={{ textAlign: 'center' }}>
              <span>外网使用时段:</span>
              <RangePicker
                autoFocus
                showTime
                format="YYYY-MM-DD HH:mm:ss"
                allowClear={false}
                value={rangePickerValue}
                onChange={this.handleRangePickerChange}
                style={{ width: 340, marginLeft: 20 }}
              />
            </Col>
          </Row>
        </Modal>
      </Fragment>
    );
  }
}
