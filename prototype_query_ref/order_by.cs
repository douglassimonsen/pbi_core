namespace Microsoft.InfoNav.Data.Contracts.Internal
{
  [DataContract(Name = "SortClause", Namespace = "http://schemas.microsoft.com/sqlbi/2013/01/NLRuntimeService")]
  public sealed class QuerySortClause
  {
    [DataMember(IsRequired = true, Order = 1)]
    public QueryExpressionContainer Expression { get; set; }

    [DataMember(IsRequired = true, Order = 2)]
    public QuerySortDirection Direction { get; set; }

    internal void WriteQueryString(QueryStringWriter w)
    {
      this.Expression.WriteQueryString(w);
      switch (this.Direction)
      {
        case QuerySortDirection.Ascending:
          w.Write(" ascending");
          break;
        case QuerySortDirection.Descending:
          w.Write(" descending");
          break;
      }
    }
  }
}
