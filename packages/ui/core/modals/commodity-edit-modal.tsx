import {
  CurrencyCodeEnum,
  DEFAULT_COMMODITY_CONTENT,
  MetadataObjectTypeEnum,
  OrderFilter,
  WeightUnitEnum,
} from "@karrio/types";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "../forms/metadata-editor";
import { isEqual, isNone, validationMessage, validityCheck } from "@karrio/lib";
import { CommodityType, CURRENCY_OPTIONS, WEIGHT_UNITS } from "@karrio/types";
import React, { useContext, useReducer, useState } from "react";
import { TextAreaField } from "../components/textarea-field";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { LineItemInput } from "../forms/line-item-input";
import { InputField } from "../components/input-field";
import { CountryInput } from "../forms/country-input";
import { Notifier } from "../components/notifier";
import { Loading } from "../components/loader";
import { useOrders } from "@karrio/hooks/order";

type OperationType = {
  commodity?: CommodityType;
  onSubmit: (commodity: CommodityType) => Promise<any>;
};
type CommodityStateContextType = {
  editCommodity: (operation: OperationType) => void;
};
type stateValue = string | boolean | Partial<CommodityType> | undefined | null;

export const CommodityStateContext =
  React.createContext<CommodityStateContextType>(
    {} as CommodityStateContextType,
  );

interface CommodityEditModalComponent {
  children?: React.ReactNode;
  orderFilter?: OrderFilter & { isDisabled?: boolean; cacheKey?: string };
}

function reducer(
  state: any,
  { name, value }: { name: string; value: stateValue | number | boolean },
) {
  switch (name) {
    case "partial":
      return isNone(value)
        ? undefined
        : { ...(state || {}), ...(value as CommodityType) };
    case "value_amount":
      const value_currency = isNone(value)
        ? state.value_currency
        : CurrencyCodeEnum.USD;
      return { ...state, [name]: value, value_currency };
    default:
      return { ...state, [name]: value };
  }
}

export const CommodityEditModalProvider = ({
  children,
  orderFilter,
}: CommodityEditModalComponent): JSX.Element => {
  const {
    metadata: { ORDERS_MANAGEMENT },
  } = useAPIMetadata();
  const { loading, setLoading } = useContext(Loading);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`commodity-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [commodity, dispatch] = useReducer(
    reducer,
    undefined,
    () => DEFAULT_COMMODITY_CONTENT,
  );
  const [operation, setOperation] = useState<OperationType | undefined>();
  const [isInvalid, setIsInvalid] = useState<boolean>(false);
  const [maxQty, setMaxQty] = useState<number | null | undefined>();
  const { query } = useOrders({
    first: 10,
    status: ["unfulfilled", "partial"] as any,
    isDisabled: !ORDERS_MANAGEMENT,
    ...(orderFilter || {}),
  });

  const editCommodity = (operation: OperationType) => {
    const commodity =
      operation.commodity || (DEFAULT_COMMODITY_CONTENT as CommodityType);

    setIsActive(true);
    setOperation(operation);
    setIsNew(isNone(operation.commodity));
    dispatch({ name: "partial", value: commodity });
    setKey(`commodity-${Date.now()}`);
  };
  const close = (_?: React.MouseEvent) => {
    setIsActive(false);
    setOperation(undefined);
    dispatch({ name: "partial", value: undefined });
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | any>) => {
    event.preventDefault();
    const target = event.target;
    let name: string = target.name;
    let value: stateValue =
      target.type === "checkbox" ? target.checked : target.value;

    dispatch({
      name,
      value: target.type === "number" ? parseFloat(value as string) : value,
    });
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    commodity.id && setLoading(true);
    operation?.onSubmit &&
      (await operation?.onSubmit(commodity as CommodityType));
    setTimeout(() => {
      commodity.id && setLoading(false);
      close();
    }, 500);
  };
  const loadLineItem = (item?: CommodityType | any) => {
    const {
      id: parent_id,
      unfulfilled_quantity: quantity,
      ...content
    } = item || { id: null };
    setMaxQty(quantity);
    dispatch({ name: "partial", value: { ...content, parent_id, quantity } });
  };

  return (
    <Notifier>
      <CommodityStateContext.Provider value={{ editCommodity }}>
        {children}
      </CommodityStateContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <div className="modal-card max-modal-height">
          <section className="modal-card-body modal-form">
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">
                {isNew ? "Add" : "Update"} commodity
              </span>
            </div>
            <div className="p-3 my-4"></div>

            {commodity !== undefined && (
              <>
                <div
                  className="px-0 py-4"
                  key={key}
                  onChange={(e: any) => {
                    setIsInvalid(
                      e.currentTarget.querySelectorAll(".is-danger").length > 0,
                    );
                  }}
                >
                  {ORDERS_MANAGEMENT && (
                    <div className="columns is-multiline mb-4 px-1">
                      <LineItemInput
                        name="parent_id"
                        label="Order Line Item"
                        value={commodity?.parent_id}
                        onChange={loadLineItem}
                        query={query}
                        onReady={(_: any) => setMaxQty(_?.unfulfilled_quantity)}
                        dropdownClass="is-small"
                        fieldClass="mb-0 p-0"
                        wrapperClass="column is-11 pl-2 pr-0 py-1"
                        className="is-small is-fullwidth"
                        placeholder="Link an order line item"
                      />

                      <div className="column m-0 px-0 py-1 is-flex is-align-items-flex-end">
                        <button
                          type="button"
                          className="button is-white is-small"
                          disabled={isNone(commodity?.parent_id)}
                          title="unlink order line item"
                          onClick={() => {
                            dispatch({ name: "parent_id", value: null });
                            setMaxQty(undefined);
                          }}
                        >
                          <span className="icon is-small">
                            <i className="fas fa-unlink"></i>
                          </span>
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="columns is-multiline mb-4 px-1">
                    <InputField
                      name="title"
                      label="Title"
                      placeholder="IPod Nano"
                      onChange={handleChange}
                      value={commodity?.title}
                      className="is-small is-fullwidth"
                      wrapperClass="column is-12 px-2 py-1"
                      fieldClass="mb-0 p-0"
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                    />
                  </div>

                  <div className="columns is-multiline mb-4 px-1">
                    <InputField
                      name="hs_code"
                      label="HS code"
                      placeholder="000000"
                      onChange={handleChange}
                      value={commodity?.hs_code}
                      className="is-small is-fullwidth"
                      wrapperClass="column is-12 px-2 py-1"
                      fieldClass="mb-0 p-0"
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                    />
                  </div>

                  <div className="columns is-multiline mb-4 px-1">
                    <InputField
                      name="sku"
                      label="SKU"
                      value={commodity?.sku}
                      onChange={handleChange}
                      className="is-small is-fullwidth"
                      wrapperClass="column is-7 px-2 py-1"
                      fieldClass="mb-0 p-0"
                      placeholder="0000001"
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                    />

                    <CountryInput
                      label="Origin Country"
                      className="is-small"
                      value={commodity.origin_country}
                      onValueChange={(value) =>
                        dispatch({
                          name: "origin_country",
                          value: value as string,
                        })
                      }
                      disabled={!isNone(commodity?.parent_id)}
                    />
                  </div>

                  <div className="columns is-multiline mb-4 px-1">
                    <InputField
                      label="Quantity"
                      name="quantity"
                      type="number"
                      min="1"
                      step="1"
                      className="is-small"
                      wrapperClass="column is-3 px-2 py-1"
                      fieldClass="mb-0 p-0"
                      onChange={handleChange}
                      value={commodity?.quantity}
                      onInvalid={validityCheck(
                        validationMessage("Please enter a valid quantity"),
                      )}
                      {...(isNone(maxQty) ? {} : { max: maxQty as number })}
                      required
                    />

                    <div className="column is-4 mb-0 px-2 py-1">
                      <label
                        className="label is-capitalized"
                        style={{ fontSize: ".8em" }}
                      >
                        Weight
                        <span className="icon is-small has-text-danger small-icon">
                          <i
                            className="fas fa-asterisk"
                            style={{ fontSize: ".7em" }}
                          ></i>
                        </span>
                      </label>
                      <div className="field has-addons">
                        <p className="control is-expanded">
                          <input
                            min="0"
                            step="any"
                            name="weight"
                            type="number"
                            className="input is-small"
                            onChange={handleChange}
                            value={commodity.weight}
                            disabled={!isNone(commodity?.parent_id)}
                            onInvalid={validityCheck(
                              validationMessage("Please enter a valid weight"),
                            )}
                            required
                          />
                        </p>
                        <p className="control">
                          <span className="select is-small">
                            <select
                              name="weight_unit"
                              onChange={handleChange}
                              value={commodity.weight_unit || WeightUnitEnum.KG}
                              disabled={!isNone(commodity?.parent_id)}
                            >
                              {WEIGHT_UNITS.map((unit) => (
                                <option key={unit} value={unit}>
                                  {unit}
                                </option>
                              ))}
                            </select>
                          </span>
                        </p>
                      </div>
                    </div>

                    <div className="column is-5 mb-0 px-2 py-1">
                      <label
                        className="label is-capitalized"
                        style={{ fontSize: ".8em" }}
                      >
                        Value Amount
                      </label>
                      <div className="field has-addons">
                        <p className="control is-expanded">
                          <input
                            min="0"
                            step="any"
                            type="number"
                            name="value_amount"
                            className="input is-small"
                            onChange={handleChange}
                            value={commodity.value_amount || ""}
                            disabled={!isNone(commodity?.parent_id)}
                          />
                        </p>
                        <p className="control">
                          <span className="select is-small">
                            <select
                              name="value_currency"
                              onChange={handleChange}
                              value={
                                commodity.value_currency || CurrencyCodeEnum.USD
                              }
                              required={!isNone(commodity?.value_amount)}
                              disabled={!isNone(commodity?.parent_id)}
                            >
                              {CURRENCY_OPTIONS.map((unit) => (
                                <option key={unit} value={unit}>
                                  {unit}
                                </option>
                              ))}
                            </select>
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="columns is-multiline mb-0 px-1">
                    {/* @ts-ignore */}
                    <TextAreaField
                      name="description"
                      label="description"
                      className="is-small"
                      fieldClass="column mb-0 is-12 px-2 py-1"
                      placeholder="item description"
                      rows={2}
                      maxLength={100}
                      onChange={handleChange}
                      value={commodity?.description}
                      disabled={!isNone(commodity?.parent_id)}
                    />
                  </div>

                  <hr className="mt-1 my-3" style={{ height: "1px" }} />

                  <MetadataEditor
                    id={commodity.id}
                    object_type={MetadataObjectTypeEnum.commodity}
                    metadata={commodity.metadata}
                    onChange={(value) => dispatch({ name: "metadata", value })}
                  >
                    {(() => {
                      const { isEditing, editMetadata } = useContext(
                        MetadataEditorContext,
                      );

                      return (
                        <>
                          <div className="is-flex is-justify-content-space-between">
                            <h2 className="title is-6 my-3">Metadata</h2>

                            <button
                              type="button"
                              className="button is-default is-small is-align-self-center"
                              disabled={isEditing}
                              onClick={() => editMetadata()}
                            >
                              <span className="icon is-small">
                                <i className="fas fa-pen"></i>
                              </span>
                              <span>Edit metadata</span>
                            </button>
                          </div>

                          <hr className="mt-1 my-1" style={{ height: "1px" }} />
                        </>
                      );
                    })()}
                  </MetadataEditor>
                </div>

                <div className="p-3 my-5"></div>
                <div className="form-floating-footer has-text-centered p-1">
                  <button
                    className="button is-default m-1 is-small"
                    onClick={close}
                    disabled={loading}
                  >
                    <span>Cancel</span>
                  </button>
                  <button
                    className={`button is-primary ${loading ? "is-loading" : ""} m-1 is-small`}
                    disabled={
                      loading ||
                      isInvalid ||
                      isEqual(operation?.commodity, commodity)
                    }
                    onClick={handleSubmit}
                  >
                    <span>{isNew ? "Add" : "Save"}</span>
                  </button>
                </div>
              </>
            )}
          </section>
        </div>

        <button
          className="modal-close is-large has-background-dark"
          aria-label="close"
          onClick={close}
        ></button>
      </div>
    </Notifier>
  );
};

export function useCommodityEditModal() {
  return React.useContext(CommodityStateContext);
}
