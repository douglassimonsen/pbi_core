namespace Microsoft.InfoNav.Data.Contracts.Internal
{
  [DataContract(Name = "Expression", Namespace = "http://schemas.microsoft.com/sqlbi/2013/01/NLRuntimeService")]
  public sealed class QueryExpressionContainer : IEquatable<QueryExpressionContainer>
  {
    private QueryExpression _expression;

    public QueryExpressionContainer()
    {
    }

    public QueryExpressionContainer(
      QueryExpression expression,
      string name = null,
      string nativeReferenceName = null)
    {
      Contract.CheckParam(expression != (QueryExpression) null, nameof (expression));
      this.SetExpression(expression);
      this.Name = name;
      this.NativeReferenceName = nativeReferenceName;
    }

    [DataMember(IsRequired = false, Order = 1, EmitDefaultValue = false)]
    public QuerySourceRefExpression SourceRef
    {
      get => this.GetExpression<QuerySourceRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    public QueryPropertyExpression Property
    {
      get => this.GetExpression<QueryPropertyExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Name = "Property", Order = 2, EmitDefaultValue = false)]
    private QueryPropertyExpression PropertyContract
    {
      get
      {
        QueryPropertyExpression expression = this.GetExpression<QueryPropertyExpression>();
        return !((QueryExpression) expression != (QueryExpression) null) || !(expression.GetType() == typeof (QueryPropertyExpression)) ? (QueryPropertyExpression) null : expression;
      }
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 3, EmitDefaultValue = false)]
    public QueryAndExpression And
    {
      get => this.GetExpression<QueryAndExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 4, EmitDefaultValue = false)]
    public QueryOrExpression Or
    {
      get => this.GetExpression<QueryOrExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 5, EmitDefaultValue = false)]
    public QueryContainsExpression Contains
    {
      get => this.GetExpression<QueryContainsExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 6, EmitDefaultValue = false)]
    public QueryComparisonExpression Comparison
    {
      get => this.GetExpression<QueryComparisonExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 7, EmitDefaultValue = false)]
    public QueryBetweenExpression Between
    {
      get => this.GetExpression<QueryBetweenExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 8, EmitDefaultValue = false)]
    public QueryInExpression In
    {
      get => this.GetExpression<QueryInExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 8, EmitDefaultValue = false)]
    public QueryAggregationExpression Aggregation
    {
      get => this.GetExpression<QueryAggregationExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 9, EmitDefaultValue = false)]
    public QueryExistsExpression Exists
    {
      get => this.GetExpression<QueryExistsExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 10, EmitDefaultValue = false)]
    public QueryDatePartExpression DatePart
    {
      get => this.GetExpression<QueryDatePartExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 11, EmitDefaultValue = false)]
    public QueryBooleanConstantExpression Boolean
    {
      get => this.GetExpression<QueryBooleanConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 12, EmitDefaultValue = false)]
    public QueryIntegerConstantExpression Integer
    {
      get => this.GetExpression<QueryIntegerConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 13, EmitDefaultValue = false)]
    public QueryDecimalConstantExpression Decimal
    {
      get => this.GetExpression<QueryDecimalConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 14, EmitDefaultValue = false)]
    public QueryStringConstantExpression String
    {
      get => this.GetExpression<QueryStringConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 15, EmitDefaultValue = false)]
    public QueryDateTimeConstantExpression DateTime
    {
      get => this.GetExpression<QueryDateTimeConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 16, EmitDefaultValue = false)]
    public QueryDateConstantExpression Date
    {
      get => this.GetExpression<QueryDateConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 19, EmitDefaultValue = false)]
    public QueryYearConstantExpression Year
    {
      get => this.GetExpression<QueryYearConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 20, EmitDefaultValue = false)]
    public QueryDecadeConstantExpression Decade
    {
      get => this.GetExpression<QueryDecadeConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 21, EmitDefaultValue = false)]
    public QueryYearAndMonthConstantExpression YearAndMonth
    {
      get => this.GetExpression<QueryYearAndMonthConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 22, EmitDefaultValue = false)]
    public QueryNotExpression Not
    {
      get => this.GetExpression<QueryNotExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 23, EmitDefaultValue = false)]
    public QueryNullConstantExpression Null
    {
      get => this.GetExpression<QueryNullConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 24, EmitDefaultValue = false)]
    public QueryStartsWithExpression StartsWith
    {
      get => this.GetExpression<QueryStartsWithExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 25, EmitDefaultValue = false)]
    public QueryDateTimeSecondConstantExpression DateTimeSecond
    {
      get => this.GetExpression<QueryDateTimeSecondConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 26, EmitDefaultValue = false)]
    public QueryNumberConstantExpression Number
    {
      get => this.GetExpression<QueryNumberConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 27, EmitDefaultValue = false)]
    public QueryDateAddExpression DateAdd
    {
      get => this.GetExpression<QueryDateAddExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 28, EmitDefaultValue = false)]
    public QueryNowExpression Now
    {
      get => this.GetExpression<QueryNowExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 29, EmitDefaultValue = false)]
    public QueryYearAndWeekConstantExpression YearAndWeek
    {
      get => this.GetExpression<QueryYearAndWeekConstantExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 30, EmitDefaultValue = false)]
    public QueryDateSpanExpression DateSpan
    {
      get => this.GetExpression<QueryDateSpanExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 31, EmitDefaultValue = false)]
    public QueryLiteralExpression Literal
    {
      get => this.GetExpression<QueryLiteralExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 32, EmitDefaultValue = false)]
    public QueryColumnExpression Column
    {
      get => this.GetExpression<QueryColumnExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 33, EmitDefaultValue = false)]
    public QueryMeasureExpression Measure
    {
      get => this.GetExpression<QueryMeasureExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 34, EmitDefaultValue = false)]
    public QueryPercentileExpression Percentile
    {
      get => this.GetExpression<QueryPercentileExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 35, EmitDefaultValue = false)]
    public QueryHierarchyExpression Hierarchy
    {
      get => this.GetExpression<QueryHierarchyExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 36, EmitDefaultValue = false)]
    public QueryHierarchyLevelExpression HierarchyLevel
    {
      get => this.GetExpression<QueryHierarchyLevelExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 37, EmitDefaultValue = false)]
    public QueryDefaultValueExpression DefaultValue
    {
      get => this.GetExpression<QueryDefaultValueExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 38, EmitDefaultValue = false)]
    public QueryAnyValueExpression AnyValue
    {
      get => this.GetExpression<QueryAnyValueExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 39, EmitDefaultValue = false)]
    public QueryPropertyVariationSourceExpression PropertyVariationSource
    {
      get => this.GetExpression<QueryPropertyVariationSourceExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 40, EmitDefaultValue = false)]
    public QueryArithmeticExpression Arithmetic
    {
      get => this.GetExpression<QueryArithmeticExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 41, EmitDefaultValue = false)]
    public QueryScopedEvalExpression ScopedEval
    {
      get => this.GetExpression<QueryScopedEvalExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 42, EmitDefaultValue = false)]
    public QueryTransformTableRefExpression TransformTableRef
    {
      get => this.GetExpression<QueryTransformTableRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 43, EmitDefaultValue = false)]
    public QueryTransformOutputRoleRefExpression TransformOutputRoleRef
    {
      get => this.GetExpression<QueryTransformOutputRoleRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 44, EmitDefaultValue = false)]
    public QuerySubqueryExpression Subquery
    {
      get => this.GetExpression<QuerySubqueryExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 45, EmitDefaultValue = false)]
    public QueryFloorExpression Floor
    {
      get => this.GetExpression<QueryFloorExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 46, EmitDefaultValue = false)]
    public QueryDiscretizeExpression Discretize
    {
      get => this.GetExpression<QueryDiscretizeExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 48, EmitDefaultValue = false)]
    public QueryMemberExpression Member
    {
      get => this.GetExpression<QueryMemberExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 49, EmitDefaultValue = false)]
    public QueryFilteredEvalExpression FilteredEval
    {
      get => this.GetExpression<QueryFilteredEvalExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 50, EmitDefaultValue = false)]
    public QueryEndsWithExpression EndsWith
    {
      get => this.GetExpression<QueryEndsWithExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 51, EmitDefaultValue = false)]
    public QueryNativeFormatExpression NativeFormat
    {
      get => this.GetExpression<QueryNativeFormatExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 52, EmitDefaultValue = false)]
    public QueryNativeMeasureExpression NativeMeasure
    {
      get => this.GetExpression<QueryNativeMeasureExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 53, EmitDefaultValue = false)]
    public QueryLetRefExpression LetRef
    {
      get => this.GetExpression<QueryLetRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 54, EmitDefaultValue = false)]
    public QueryRoleRefExpression RoleRef
    {
      get => this.GetExpression<QueryRoleRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 55, EmitDefaultValue = false)]
    public QuerySummaryValueRefExpression SummaryValueRef
    {
      get => this.GetExpression<QuerySummaryValueRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 56, EmitDefaultValue = false)]
    public QueryParameterRefExpression ParameterRef
    {
      get => this.GetExpression<QueryParameterRefExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 57, EmitDefaultValue = false)]
    public QueryTableTypeExpression TableType
    {
      get => this.GetExpression<QueryTableTypeExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 58, EmitDefaultValue = false)]
    public QueryPrimitiveTypeExpression PrimitiveType
    {
      get => this.GetExpression<QueryPrimitiveTypeExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 59, EmitDefaultValue = false)]
    public QueryTypeOfExpression TypeOf
    {
      get => this.GetExpression<QueryTypeOfExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 60, EmitDefaultValue = false)]
    public QuerySparklineDataExpression SparklineData
    {
      get => this.GetExpression<QuerySparklineDataExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 61, EmitDefaultValue = false)]
    public QueryNativeVisualCalculationExpression NativeVisualCalculation
    {
      get => this.GetExpression<QueryNativeVisualCalculationExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 62, EmitDefaultValue = false)]
    public QueryMinExpression Min
    {
      get => this.GetExpression<QueryMinExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 63, EmitDefaultValue = false)]
    public QueryMaxExpression Max
    {
      get => this.GetExpression<QueryMaxExpression>();
      set => this.SetExpression((QueryExpression) value);
    }

    [DataMember(IsRequired = false, Order = 998, EmitDefaultValue = false)]
    public string NativeReferenceName { get; set; }

    [DataMember(IsRequired = false, Order = 999, EmitDefaultValue = false)]
    public string Name { get; set; }

    public QueryConstantExpression Constant => this.GetExpression<QueryConstantExpression>();

    public QueryExpression Expression => this._expression;

    public override string ToString() => this.ToString(false, false);

    public string ToSafeTraceString() => this.ToString(true, false);

    public string ToTraceStringWithCustomerContent() => this.ToString(true, true);

    internal void ReplaceExpression(QueryExpression expression)
    {
      this._expression = (QueryExpression) null;
      this.SetExpression(expression);
    }

    internal void WriteQueryString(QueryStringWriter w)
    {
      try
      {
        this._expression.WriteQueryString(w);
        if (w.EmitExpressionNames && !string.IsNullOrEmpty(this.Name))
        {
          w.Write(" as ");
          w.WriteIdentifierCustomerContent(this.Name);
        }
        if (!w.EmitExpressionNames || string.IsNullOrEmpty(this.NativeReferenceName))
          return;
        w.Write(" with nativereferencename ");
        w.WriteIdentifierCustomerContent(this.NativeReferenceName);
      }
      catch (Exception ex) when (!ex.IsStoppingException())
      {
        if (w.TraceString)
          w.Write(ex.ToString());
        throw;
      }
    }

    private string ToString(bool traceString, bool includeMarkedUpCustomerContent)
    {
      QueryStringWriter w = new QueryStringWriter(false, traceString, includeMarkedUpCustomerContent);
      this.WriteQueryString(w);
      return w.ToString();
    }

    private TExpression GetExpression<TExpression>() where TExpression : QueryExpression
    {
      return this._expression as TExpression;
    }

    private void SetExpression(QueryExpression expression)
    {
      Contract.CheckParam(this._expression == (QueryExpression) null || (object) this._expression == (object) expression, nameof (expression), "An expression container can only have a single value");
      this._expression = expression;
    }

    public static implicit operator QueryExpressionContainer(QueryExpression value)
    {
      return !(value == (QueryExpression) null) ? new QueryExpressionContainer(value) : (QueryExpressionContainer) null;
    }

    public override bool Equals(object obj) => this.Equals(obj as QueryExpressionContainer);

    public override int GetHashCode()
    {
      return this.Name != null || this.NativeReferenceName != null ? Hashing.CombineHash(Hashing.GetHashCode<string>(this.Name, (IEqualityComparer<string>) ConceptualNameComparer.Instance), Hashing.GetHashCode<string>(this.NativeReferenceName, (IEqualityComparer<string>) ConceptualNameComparer.Instance), Hashing.GetHashCode<QueryExpression>(this.Expression)) : Hashing.GetHashCode<QueryExpression>(this.Expression);
    }

    public bool Equals(QueryExpressionContainer other)
    {
      bool? nullable = Util.AreEqual<QueryExpressionContainer>(this, other);
      if (nullable.HasValue)
        return nullable.Value;
      if (!ConceptualNameComparer.Instance.Equals(this.Name, other.Name) || !ConceptualNameComparer.Instance.Equals(this.NativeReferenceName, other.NativeReferenceName) || this.Expression == (QueryExpression) null != (other.Expression == (QueryExpression) null))
        return false;
      return this.Expression == (QueryExpression) null || this.Expression.Equals(other.Expression);
    }

    public static bool operator ==(QueryExpressionContainer left, QueryExpressionContainer right)
    {
      bool? nullable = Util.AreEqual<QueryExpressionContainer>(left, right);
      return nullable.HasValue ? nullable.Value : left.Equals(right);
    }

    public static bool operator !=(QueryExpressionContainer left, QueryExpressionContainer right)
    {
      return !(left == right);
    }
  }
}
