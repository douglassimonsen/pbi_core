namespace Microsoft.InfoNav.Data.Contracts.Internal
{
  [DataContract(Name = "Transform", Namespace = "http://schemas.microsoft.com/sqlbi/2013/01/NLRuntimeService")]
  public sealed class QueryTransform
  {
    [DataMember(IsRequired = true, Order = 1)]
    public string Name { get; set; }

    [DataMember(IsRequired = true, Order = 2)]
    public string Algorithm { get; set; }

    [DataMember(IsRequired = true, Order = 3)]
    public QueryTransformInput Input { get; set; }

    [DataMember(IsRequired = true, Order = 4)]
    public QueryTransformOutput Output { get; set; }

    internal void WriteQueryString(QueryStringWriter w)
    {
      using (w.NewClauseScope("transform", QueryStringWriter.Separator.Newline))
      {
        w.WriteFormat("via '{0}' as ", (object) this.Algorithm);
        w.WriteIdentifierCustomerContent(this.Name);
        w.WriteLine();
        using (w.NewClauseScope("with", QueryStringWriter.Separator.CommaAndNewline))
        {
          this.WriteParameters(w, this.Input.Parameters);
          this.WriteTable("inputtable", w, this.Input.Table);
          this.WriteTable("outputtable", w, this.Output.Table);
        }
      }
    }

    private void WriteParameters(QueryStringWriter w, List<QueryExpressionContainer> parameters)
    {
      if (parameters == null || parameters.Count == 0)
        return;
      w.WriteSeparator();
      QueryStringWriterUtils.WriteFunction<QueryExpressionContainer>("inputparameters", (IReadOnlyList<QueryExpressionContainer>) parameters, QueryStringWriter.Separator.Comma, (Action<QueryExpressionContainer, QueryStringWriter>) ((param, writer) => writer.WriteExpressionAndName(param)), w);
    }

    private void WriteTable(string functionName, QueryStringWriter w, QueryTransformTable table)
    {
      if (table == null)
        return;
      w.WriteSeparator();
      QueryStringWriterUtils.WriteFunction<QueryTransformTableColumn>(functionName, (IReadOnlyList<QueryTransformTableColumn>) table.Columns, QueryStringWriter.Separator.Comma, (Action<QueryTransformTableColumn, QueryStringWriter>) ((column, writer) =>
      {
        writer.WriteExpressionAndName(column.Expression);
        if (string.IsNullOrEmpty(column.Role))
          return;
        w.WriteFormat(" with role '{0}'", (object) column.Role);
      }), w);
      QueryStringWriterUtils.WriteName(table.Name, w);
    }
  }
}
