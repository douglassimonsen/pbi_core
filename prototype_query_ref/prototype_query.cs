namespace Microsoft.InfoNav.Data.Contracts.Internal
{
  [DataContract(Name = "Definition", Namespace = "http://schemas.microsoft.com/sqlbi/2013/01/NLRuntimeService")]
  public sealed class QueryDefinition : IEquatable<QueryDefinition>
  {
    private static readonly DataContractJsonSerializer _jsonSerializer = new DataContractJsonSerializer(typeof (QueryDefinition));
    private List<EntitySource> _from;

    public QueryDefinition()
    {
      this.From = new List<EntitySource>();
      this.Where = new List<QueryFilter>();
      this.OrderBy = new List<QuerySortClause>();
      this.Select = new List<QueryExpressionContainer>();
      this.GroupBy = new List<QueryExpressionContainer>();
    }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 0)]
    public int? Version { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 1)]
    public string DatabaseName { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 2)]
    public List<QueryExpressionContainer> Parameters { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 3)]
    public List<QueryExpressionContainer> Let { get; set; }

    [DataMember(IsRequired = false, Order = 4)]
    public List<EntitySource> From
    {
      get
      {
        if (this._from == null)
          this._from = new List<EntitySource>();
        return this._from;
      }
      set => this._from = value;
    }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 5)]
    public List<QueryFilter> Where { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 6)]
    public List<QuerySortClause> OrderBy { get; set; }

    [DataMember(IsRequired = true, Order = 7)]
    public List<QueryExpressionContainer> Select { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 8)]
    public List<QueryAxis> VisualShape { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 9)]
    public List<QueryExpressionContainer> GroupBy { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 10)]
    public List<QueryTransform> Transform { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 11)]
    public long? Skip { get; set; }

    [DataMember(IsRequired = false, EmitDefaultValue = false, Order = 12)]
    public int? Top { get; set; }

    public override string ToString() => this.ToString(false, false, false);

    public string ToSafeTraceString() => this.ToString(false, true, false);

    public string ToTraceStringWithCustomerContent() => this.ToString(false, true, true);

    public bool Equals(QueryDefinition other)
    {
      if ((object) other == null)
        return false;
      return (object) this == (object) other || string.Equals(this.ToString(), other.ToString(), StringComparison.Ordinal);
    }

    public override bool Equals(object other) => this.Equals(other as QueryDefinition);

    public static bool operator ==(QueryDefinition left, QueryDefinition right)
    {
      if ((object) left == null && (object) right == null)
        return true;
      return (object) left != null && left.Equals(right);
    }

    public static bool operator !=(QueryDefinition left, QueryDefinition right) => !(left == right);

    internal static QueryDefinition FromJsonString(string s)
    {
      return QueryDefinition._jsonSerializer.FromJsonString<QueryDefinition>(s);
    }

    public override int GetHashCode() => this.ToString().GetHashCode();

    internal QueryDefinition Clone()
    {
      return QueryDefinition.FromJsonString(QueryDefinition._jsonSerializer.ToJsonString((object) this));
    }

    internal string ToString(
      bool emitExpressionNames,
      bool traceString,
      bool includeMarkedUpCustomerContent,
      string[] filterRestatements = null)
    {
      QueryStringWriter w = new QueryStringWriter(emitExpressionNames, traceString, includeMarkedUpCustomerContent);
      this.WriteQueryString(w, filterRestatements);
      return w.ToString();
    }

    internal string ToJsonString() => QueryDefinition._jsonSerializer.ToJsonString((object) this);

    internal void WriteQueryString(QueryStringWriter w, string[] filterRestatements = null)
    {
      using (w.NewSeparatorScope(QueryStringWriter.Separator.Newline))
      {
        QueryStringWriterUtils.WriteParameters(this.Parameters, w);
        QueryStringWriterUtils.WriteLet(this.Let, w);
        QueryStringWriterUtils.WriteFrom(this.From, w);
        QueryStringWriterUtils.WriteWhere(this.Where, w, filterRestatements);
        this.WriteTransform(w);
        this.WriteOrderBy(w);
        this.WriteSelect(w);
        QueryStringWriterUtils.WriteVisualShape(this.VisualShape, w);
        this.WriteGroupBy(w);
        this.WriteSkip(w);
        this.WriteTop(w);
      }
    }

    private void WriteTransform(QueryStringWriter w)
    {
      if (this.Transform == null || this.Transform.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewSeparatorScope(QueryStringWriter.Separator.Newline))
      {
        foreach (QueryTransform transform in this.Transform)
        {
          w.WriteSeparator();
          if (transform == null || !QueryDefinitionValidator.IsValid(transform))
          {
            using (w.NewClauseScope("transform", QueryStringWriter.Separator.Newline))
              w.WriteError();
          }
          else
            transform.WriteQueryString(w);
        }
      }
    }

    private void WriteOrderBy(QueryStringWriter w)
    {
      if (this.OrderBy == null || this.OrderBy.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewClauseScope("orderby", QueryStringWriter.Separator.Comma))
      {
        foreach (QuerySortClause sortClause in this.OrderBy)
        {
          w.WriteSeparator();
          if (sortClause == null || !QueryDefinitionValidator.IsValid(sortClause))
            w.WriteError();
          else
            sortClause.WriteQueryString(w);
        }
      }
    }

    private void WriteSelect(QueryStringWriter w)
    {
      if (this.Select == null || this.Select.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewClauseScope("select", QueryStringWriter.Separator.Comma))
      {
        foreach (QueryExpressionContainer expression in this.Select)
        {
          w.WriteSeparator();
          if (expression == (QueryExpressionContainer) null || !QueryExpressionValidator.IsValid(expression))
            w.WriteError();
          else
            expression.WriteQueryString(w);
        }
      }
    }

    private void WriteGroupBy(QueryStringWriter w)
    {
      if (this.GroupBy == null || this.GroupBy.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewClauseScope("groupby", QueryStringWriter.Separator.Comma))
      {
        foreach (QueryExpressionContainer expression in this.GroupBy)
        {
          w.WriteSeparator();
          if (expression == (QueryExpressionContainer) null || !QueryExpressionValidator.IsValid(expression))
            w.WriteError();
          else
            expression.WriteQueryString(w);
        }
      }
    }

    private void WriteTop(QueryStringWriter w)
    {
      if (!this.Top.HasValue)
        return;
      w.WriteSeparator();
      w.Write("top " + this.Top.Value.ToString());
    }

    private void WriteSkip(QueryStringWriter w)
    {
      if (!this.Skip.HasValue)
        return;
      w.WriteSeparator();
      w.Write("skip " + this.Skip.Value.ToString());
    }
  }
}
