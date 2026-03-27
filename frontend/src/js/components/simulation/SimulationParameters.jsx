import { Collapse, Form, InputNumber } from "antd";

/**
 * A function to allow the user to customize attributes of the simulation
 *
 * @typedef {object} simParams
 * @property {number} starting_distance The distance between the players and
 *  enemies at the start of the encounter
 * @property {number} health_multiplier The multipplier applied to the players'
 *  hit points at the start of the encounter
 *
 * @param {object} props
 * @param {simParams} props.parameters The object containing the values for
 *  the parameters
 * @param {function} props.setParameters The function to set the value of
 *  `parameters`
 * @returns
 */
export default function SimulationParameters({ parameters, setParameters }) {
  const [form] = Form.useForm();

  const collapseItems = [
    {
      key: "sim_params",
      label: "Other Simulation Parameters",
      children: (
        <Form
          form={form}
          name="parameters"
          initialValues={parameters}
          onValuesChange={() => {
            const allValues = form.getFieldsValue(true);
            setParameters(allValues);
          }}
        >
          <Form.Item label="Starting Distance" name="starting_distance">
            <InputNumber min={10} max={500} step={5} />
          </Form.Item>
          <Form.Item label="Player Health Multiplier" name="health_multiplier">
            <InputNumber min={0.05} max={1} step={0.05} />
          </Form.Item>
        </Form>
      ),
    },
  ];

  return <Collapse items={collapseItems} size="small" />;
}
