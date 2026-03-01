import {
  Button,
  Card,
  Col,
  Form,
  Input,
  InputNumber,
  Row,
  Select,
  Switch,
} from "antd";
import { ClearOutlined } from "@ant-design/icons";

import { traitOptions } from "./enemyHelpers";
import { damageTypes } from "../../characters/characterHelpers";

/**
 * A component to display a filter form for the enemy list
 *
 * @param {object} props
 * @param {object} props.form The Ant Design form instance
 * @returns {React.ReactElement}
 */
export default function EnemyFilterForm({ form }) {
  const initialValues = {
    name: "",
    minLevel: -1,
    maxLevel: 5,
    traits: [],
    traitFilterMode: false, // false = ANY (OR), true = ALL (AND)
    immunities: [],
    immunitiesFilterMode: false,
  };

  const currentMinLevel = Form.useWatch("minLevel", form);
  const currentMaxLevel = Form.useWatch("maxLevel", form);

  function handleClear() {
    form.resetFields();
  }

  return (
    <Card style={{ marginBottom: 16 }}>
      <Form
        form={form}
        initialValues={initialValues}
        layout="vertical"
        autoComplete="off"
      >
        <Row gutter={[16, 0]}>
          <Col xs={24} sm={12} md={8}>
            <Form.Item label="Name" name="name" style={{ marginBottom: 0 }}>
              <Input placeholder="Search by name" allowClear />
            </Form.Item>
          </Col>

          <Col xs={24} sm={12} md={8}>
            <Form.Item
              label="Min Level"
              name="minLevel"
              style={{ marginBottom: 0 }}
            >
              <InputNumber
                min={-1}
                max={currentMaxLevel}
                style={{ width: "100%" }}
                placeholder="Min"
              />
            </Form.Item>
          </Col>

          <Col xs={24} sm={12} md={8}>
            <Form.Item
              label="Max Level"
              name="maxLevel"
              style={{ marginBottom: 0 }}
            >
              <InputNumber
                min={currentMinLevel}
                max={5}
                style={{ width: "100%" }}
                placeholder="Max"
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={[16, 0]} style={{ marginTop: 16 }}>
          <Col xs={24} md={20}>
            <Form.Item label="Traits" name="traits" style={{ marginBottom: 0 }}>
              <Select
                mode="multiple"
                allowClear
                placeholder="Filter by traits"
                options={traitOptions}
              />
            </Form.Item>
          </Col>

          <Col xs={24} md={4}>
            <Form.Item
              label="Match any/all?"
              name="traitFilterMode"
              valuePropName="checked"
              style={{ marginBottom: 0 }}
            >
              <Switch checkedChildren="All" unCheckedChildren="Any" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={[16, 0]} style={{ marginTop: 16 }}>
          <Col xs={24} md={20}>
            <Form.Item
              label="Immunities"
              name="immunities"
              style={{ marginBottom: 0 }}
            >
              <Select
                mode="multiple"
                allowClear
                placeholder="Filter by immunities"
                options={damageTypes}
              />
            </Form.Item>
          </Col>

          <Col xs={24} md={4}>
            <Form.Item
              label="Match any/all?"
              name="immunitiesFilterMode"
              valuePropName="checked"
              style={{ marginBottom: 0 }}
            >
              <Switch checkedChildren="All" unCheckedChildren="Any" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={[16, 0]} style={{ marginTop: 16 }}>
          <Col xs={24} md={20}>
            <Form.Item
              label="Weaknesses"
              name="weaknesses"
              style={{ marginBottom: 0 }}
            >
              <Select
                mode="multiple"
                allowClear
                placeholder="Filter by weaknesses"
                options={damageTypes}
              />
            </Form.Item>
          </Col>

          <Col xs={24} md={4}>
            <Form.Item
              label="Match any/all?"
              name="weaknessesFilterMode"
              valuePropName="checked"
              style={{ marginBottom: 0 }}
            >
              <Switch checkedChildren="All" unCheckedChildren="Any" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={[16, 0]} style={{ marginTop: 16 }}>
          <Col xs={24} md={20}>
            <Form.Item
              label="Resistances"
              name="resistances"
              style={{ marginBottom: 0 }}
            >
              <Select
                mode="multiple"
                allowClear
                placeholder="Filter by resistances"
                options={damageTypes}
              />
            </Form.Item>
          </Col>

          <Col xs={24} md={4}>
            <Form.Item
              label="Match any/all?"
              name="resistancesFilterMode"
              valuePropName="checked"
              style={{ marginBottom: 0 }}
            >
              <Switch checkedChildren="All" unCheckedChildren="Any" />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={[16, 0]} style={{ marginTop: 16 }}>
          <Col xs={24}>
            <Button
              icon={<ClearOutlined />}
              type="primary"
              danger
              onClick={handleClear}
              block
            >
              Reset Filters
            </Button>
          </Col>
        </Row>
      </Form>
    </Card>
  );
}
