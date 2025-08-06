namespace Microsoft.InfoNav.Data.Contracts.Internal
{
  internal static class QueryStringWriterUtils
  {
    internal static void WriteParameters(
      List<QueryExpressionContainer> parameterDeclarations,
      QueryStringWriter w)
    {
      QueryStringWriterUtils.WriteNamedExpressionClause("parameters", parameterDeclarations, w, new Func<QueryExpressionContainer, bool>(QueryDefinitionValidator.IsParameterDeclarationValid));
    }

    internal static void WriteLet(List<QueryExpressionContainer> letBindings, QueryStringWriter w)
    {
      QueryStringWriterUtils.WriteNamedExpressionClause("let", letBindings, w, new Func<QueryExpressionContainer, bool>(QueryDefinitionValidator.IsLetBindingValid));
    }

    private static void WriteNamedExpressionClause(
      string clause,
      List<QueryExpressionContainer> items,
      QueryStringWriter w,
      Func<QueryExpressionContainer, bool> isValid)
    {
      if (items.IsNullOrEmpty<QueryExpressionContainer>())
        return;
      w.WriteSeparator();
      using (w.NewClauseScope(clause, QueryStringWriter.Separator.CommaAndNewline))
      {
        foreach (QueryExpressionContainer expression in items)
        {
          w.WriteSeparator();
          if (expression == (QueryExpressionContainer) null || !isValid(expression))
            w.WriteError();
          else
            w.WriteExpressionAndName(expression);
        }
      }
    }

    internal static void WriteFrom(List<EntitySource> from, QueryStringWriter w)
    {
      if (from == null || from.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewClauseScope(nameof (from), QueryStringWriter.Separator.CommaAndNewline))
      {
        foreach (EntitySource source in from)
        {
          w.WriteSeparator();
          if (source == (EntitySource) null || !QueryDefinitionValidator.IsValid(source))
            w.WriteError();
          else
            source.WriteQueryString(w);
        }
      }
    }

    internal static void WriteWhere(
      List<QueryFilter> where,
      QueryStringWriter w,
      string[] filterRestatements)
    {
      if (where == null || where.Count == 0)
        return;
      w.WriteSeparator();
      using (w.NewClauseScope(nameof (where), QueryStringWriter.Separator.CommaAndNewline))
      {
        for (int index = 0; index < where.Count; ++index)
        {
          QueryFilter queryFilter = where[index];
          w.WriteSeparator();
          if (queryFilter == (QueryFilter) null || !QueryDefinitionValidator.IsValid(queryFilter))
          {
            w.WriteError();
          }
          else
          {
            string filterRestatement = filterRestatements == null || filterRestatements.Length <= index ? (string) null : filterRestatements[index];
            queryFilter.WriteQueryString(w, filterRestatement);
          }
        }
      }
    }

    internal static void WriteVisualShape(List<QueryAxis> visualShape, QueryStringWriter w)
    {
      if (visualShape.IsNullOrEmpty<QueryAxis>())
        return;
      w.WriteSeparator();
      using (w.NewClauseScope("with visualshape", QueryStringWriter.Separator.CommaAndNewline))
      {
        w.WriteLine();
        foreach (QueryAxis axis in visualShape)
        {
          if ((object) axis == null || !QueryDefinitionValidator.IsValid(axis))
          {
            w.WriteError();
          }
          else
          {
            w.WriteSeparator();
            axis.WriteQueryString(w);
          }
        }
      }
    }

    internal static void WriteFunction<TArg>(
      string functionName,
      IReadOnlyList<TArg> args,
      QueryStringWriter.Separator argumentSeparator,
      Action<TArg, QueryStringWriter> writeArg,
      QueryStringWriter w)
    {
      w.Write(functionName);
      w.Write("(");
      if (args.Count > 0)
      {
        using (w.NewIndentScope())
        {
          InsertLineIfNeeded();
          using (w.NewSeparatorScope(argumentSeparator))
          {
            foreach (TArg obj in (IEnumerable<TArg>) args)
            {
              w.WriteSeparator();
              writeArg(obj, w);
            }
          }
        }
        InsertLineIfNeeded();
      }
      w.Write(")");

      void InsertLineIfNeeded()
      {
        if (argumentSeparator != QueryStringWriter.Separator.Newline && argumentSeparator != QueryStringWriter.Separator.CommaAndNewline)
          return;
        w.WriteLine();
      }
    }

    internal static void WriteName(string name, QueryStringWriter w)
    {
      if (string.IsNullOrEmpty(name))
        return;
      w.Write(" as ");
      w.WriteIdentifierCustomerContent(name);
    }
  }
}
